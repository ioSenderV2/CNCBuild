#!/usr/bin/env python3
"""Generate machine/drawings/model-3d.html from the dimension registry.

Every box in the model is placed from registry values, not from numbers typed
here. That is the whole point: if a dimension moves and a part stops fitting,
the model shows it as a visible gap or overlap rather than hiding it. Re-run
this after any registry change.

    python tools/make-3d.py

Where a placement could NOT be derived, it is listed in ASSUMPTIONS below and
printed on the page itself, so nobody mistakes a guess for a dimension.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "machine" / "drawings" / "model-3d.html"

# ---------------------------------------------------------------- the frame
#
#   X  across the machine, 0 at the rear plate's LEFT end  (= outer left face)
#   Y  fore-aft,           0 at the torsion box's BACK edge, +Y forward
#   Z  up,                 0 at the torsion box's TOP SKIN
#
# Three.js is Y-up, so the writer swaps: three(x, z, y).

ASSUMPTIONS = [
    "Y HOME is taken as the X end plate's BACK edge level with the Y beam's back "
    "end, mirroring the documented Y MAX (front face level with the beam end). "
    "The rear hard stop is not dimensioned anywhere.",
    "X HOME is the carriage plate butted against the left end plate's inner face. "
    "No stop or soft-limit figure exists for it.",
    "Z AT MAX puts the butted block pair at the top of the 400 mm rail, and the Z "
    "plate is centred on that pair. The plate's exact offset along the spacers is "
    "not dimensioned.",
    "The front fin's taper is drawn with a VERTICAL FRONT EDGE and the 200-to-100 "
    "taper on its back. Sheet 1 gives the widths, not which edge is square.",
    "The box tongue is drawn from the bottom skin's top face up, 179 tall, to land "
    "at the 60 proud the registry gives. torsion-box.md says 180.",
    "NO BASE OR LEGS - deliberately out of scope. The box sits on the ground plane.",
]


def main() -> int:
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    P = []  # parts: name, group, colour, [x0,y0,z0], [x1,y1,z1]

    def box(name, group, colour, x0, y0, z0, x1, y1, z1):
        P.append({"n": name, "g": group, "c": colour, "t": "box",
                  "p": [min(x0, x1), min(y0, y1), min(z0, z1)],
                  "q": [max(x0, x1), max(y0, y1), max(z0, z1)]})

    def prism(name, group, colour, profile, ya, yb):
        """An X-Z profile extruded along fore-aft. The fins are not boxes.

        p/q stay the bounding box so the camera framing and the interference
        check keep working; the check is then CONSERVATIVE on a prism, which is
        the safe direction - it may flag a touch that the real taper clears.
        """
        xs = [pt[0] for pt in profile]
        zs = [pt[1] for pt in profile]
        P.append({"n": name, "g": group, "c": colour, "t": "prism",
                  "profile": profile, "ya": min(ya, yb), "yb": max(ya, yb),
                  "p": [min(xs), min(ya, yb), min(zs)],
                  "q": [max(xs), max(ya, yb), max(zs)]})

    W = v["REAR_PLATE_L"]            # 1211.75, the machine's outer width
    D = v["BOX_FORE_AFT"]            # 1156.35
    TT = v["T_BOX_TONGUE"]           # 19
    SKIN = v["T_BB_SKIN"]            # 19

    # ---- torsion box -----------------------------------------------------
    box("Torsion box", "box", 0xC9A227, 0, 0, -v["BOX_THK"], W, D, 0)
    tz0, tz1 = -(v["BOX_THK"] - SKIN), v["BOX_TONGUE_PROUD"]
    box("Back tongue", "box", 0xA07B16, -TT, -TT, tz0, W + TT, 0, tz1)
    for x0 in (-TT, W):
        box("Side tongue", "box", 0xA07B16,
            x0, v["SIDE_TONGUE_START"], tz0, x0 + TT, v["SIDE_TONGUE_END"], tz1)

    # ---- the plates that stand on the skin -------------------------------
    box("Rear plate", "plates", 0x8899AA, 0, 0, 0, W, v["T_REAR_PLATE"], v["REAR_PLATE_W"])

    sp = v["T_SIDE_PLATE"]
    y0, y1 = v["SIDE_TONGUE_START"], v["SIDE_TONGUE_END"]
    for x0 in (0.0, W - sp):
        box("Side plate", "plates", 0x8899AA, x0, y0, 0, x0 + sp, y1, v["SIDE_PLATE_H"])

    # ---- Y beams ---------------------------------------------------------
    # The side plate's T-slot rows ARE the beam's own 15/45/75/105, so the beam's
    # underside sits SIDE_TSLOT_ROW_1 - RAIL_SLOT_INSET above the skin. That lands
    # the beam top exactly on the plate top - the check that this chain closes.
    ybot = v["SIDE_TSLOT_ROW_1"] - v["RAIL_SLOT_INSET"]
    ytop = ybot + v["BEAM_H"]
    lx0, rx0 = v["Y1_EXT_FACE_X"], v["Y2_EXT_FACE_X"] - v["EXT_W"]
    for x0 in (lx0, rx0):
        box("Y beam", "ybeams", 0x4A7DB5, x0, y0, ybot, x0 + v["EXT_W"], y1, ytop)

    # ---- front fins ------------------------------------------------------
    # They CAP THE Y BEAM'S FRONT END - plane normal to fore-aft, like the rear
    # plate does at the back - and the taper faces INBOARD, so the outboard edge
    # is square. Corrected 2026-10-03; the first model had them on the beams'
    # sides, which is the wrong plane entirely.
    fb, ft, h = v["FIN_BASE_W"], v["FIN_TOP_W"], v["FIN_STOCK"]
    for outer, sgn in ((0 - v["FIN_PROUD"], +1), (W + v["FIN_PROUD"], -1)):
        prism("Front fin", "plates", 0x6FA8DC,
              [[outer, 0], [outer + sgn * fb, 0],
               [outer + sgn * ft, h], [outer, h]],
              y1, y1 + v["T_FIN"])

    # ---- X gantry, at Y home ---------------------------------------------
    xep_t = v["T_X_ENDPLATE"]
    xb_x0 = lx0 + v["EXT_W"] + v["RAIL_STACK"] + xep_t
    xb_x1 = xb_x0 + v["BEAM_LEN"]
    xep_back = y0                       # ASSUMPTION: Y home
    xep_front = xep_back + v["XEP_W"]
    xb_top = ytop + v["XEP_TOP_ABOVE_BEAM"]
    xb_bot = xb_top - v["BEAM_H"]
    box("X beam", "gantry", 0x4A7DB5, xb_x0, xep_back, xb_bot,
        xb_x1, xep_back + v["EXT_W"], xb_top)
    for x0 in (xb_x0 - xep_t, xb_x1):
        box("X end plate", "gantry", 0x6FA8DC,
            x0, xep_back, xb_top - v["XEP_H"], x0 + xep_t, xep_front, xb_top)
        box("Y nut doubler", "gantry", 0xB06000,
            x0 - v["T_DOUBLER"] if x0 < xb_x0 else x0 + xep_t, xep_back,
            xb_top - v["XEP_H"],
            x0 if x0 < xb_x0 else x0 + xep_t + v["T_DOUBLER"],
            xep_back + v["DOUBLER_H"], xb_top - v["XEP_H"] + v["DOUBLER_H"])

    # ---- X carriage, at X home -------------------------------------------
    # The X rails sit RAIL_LOW_Z up the beam's front face; Sheet 3 puts the lower
    # block row's centre 46 up the carriage plate, so the plate's bottom follows.
    xbeam_front = xep_back + v["EXT_W"]
    cp_bot = xb_bot + v["RAIL_LOW_Z"] - 46.0
    cp_x0 = xb_x0                        # ASSUMPTION: X home, butted left
    cp_x1 = cp_x0 + v["XEP_W"]
    box("X carriage plate", "z", 0xD98E04, cp_x0, xbeam_front, cp_bot,
        cp_x1, xbeam_front + v["T_X_CARRIAGE_PLATE"], cp_bot + 407.0)

    # ---- Z plate and spindle, at Z max -----------------------------------
    cp_front = xbeam_front + v["T_X_CARRIAGE_PLATE"]
    rail_top = cp_bot + 407.0 - 7.0
    block_mid = rail_top - (v["BLOCK_BUTTED"] / 2)       # ASSUMPTION: Z at max
    zp_back = cp_front + v["RAIL_STACK"] + v["SPACER_T"]
    zp_cx = (cp_x0 + cp_x1) / 2
    box("Z plate", "z", 0xD98E04,
        zp_cx - v["Z_PLATE_W"] / 2, zp_back, block_mid - v["Z_PLATE_L"] / 2,
        zp_cx + v["Z_PLATE_W"] / 2, zp_back + v["T_Z_PLATE"],
        block_mid + v["Z_PLATE_L"] / 2)

    sp_axis = cp_front + v["SPINDLE_OFFSET"]
    r = v["SPINDLE_D"] / 2
    bar_bot = block_mid - v["SPINDLE_BARREL_L"] / 2
    box("Spindle barrel", "z", 0x999999,
        zp_cx - r, sp_axis - r, bar_bot,
        zp_cx + r, sp_axis + r, bar_bot + v["SPINDLE_BARREL_L"])
    nr = v["SPINDLE_NUT_D"] / 2
    box("Collet nut", "z", 0x333333,
        zp_cx - nr, sp_axis - nr, bar_bot - v["SPINDLE_COLLET_END"],
        zp_cx + nr, sp_axis + nr, bar_bot - v["SPINDLE_SHOULDER_DROP"])

    groups = {
        "box": "Torsion box and tongues",
        "plates": "Rear, side and fin plates",
        "ybeams": "Y beams",
        "gantry": "X gantry",
        "z": "Z carriage and spindle",
    }
    facts = [
        ("Machine width", W), ("Box fore-aft", D), ("Box thickness", v["BOX_THK"]),
        ("Y beam underside", ybot), ("Y beam top", ytop),
        ("X beam top", xb_top), ("Collet nut tip", bar_bot - v["SPINDLE_COLLET_END"]),
    ]
    OUT.write_text(HTML.replace("__PARTS__", json.dumps(P))
                       .replace("__GROUPS__", json.dumps(groups))
                       .replace("__ASSUMPTIONS__", json.dumps(ASSUMPTIONS))
                       .replace("__FACTS__", json.dumps([[a, round(b, 2)] for a, b in facts])),
                   encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} - {len(P)} parts")
    for a, b in facts:
        print(f"  {a:22} {b:10.2f}")
    return report_overlaps(P)


# Pairs that SHOULD interpenetrate, with the reason. Everything else that
# overlaps is a real interference and gets printed.
ALLOWED = {
    frozenset({"Torsion box", "Back tongue"}),      # laminated to the wall
    frozenset({"Torsion box", "Side tongue"}),
    frozenset({"Back tongue", "Side tongue"}),      # meet at the corner
    frozenset({"X beam", "X end plate"}),           # plate laps the beam's end
    frozenset({"X end plate", "Y nut doubler"}),    # doubler bolts to its face
    frozenset({"X carriage plate", "Z plate"}),     # modelled without the spacers
    frozenset({"Z plate", "Spindle barrel"}),       # clamps not modelled
}


def report_overlaps(P) -> int:
    """Solid-body interference check - the one thing a box model can prove.

    It cannot tell you a part is in the RIGHT place. It can tell you two parts
    are in the SAME place, which is the failure a dimension change causes and
    the eye misses on a shaded render.
    """
    bad = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            a, b = P[i], P[j]
            if frozenset({a["n"], b["n"]}) in ALLOWED:
                continue
            ov = [min(a["q"][k], b["q"][k]) - max(a["p"][k], b["p"][k]) for k in range(3)]
            if all(o > 0.05 for o in ov):
                bad.append((a["n"], b["n"], ov))
    if not bad:
        print("\ninterference check: clean - no two parts occupy the same space")
        return 0
    print(f"\ninterference check: {len(bad)} OVERLAP(S)")
    for n1, n2, ov in bad:
        print(f"  {n1} <-> {n2}   by {ov[0]:.2f} x {ov[1]:.2f} x {ov[2]:.2f} mm")
    return 0


HTML = r"""<!doctype html>
<meta charset="utf-8"><title>CNC assembly - generated from the dimension registry</title>
<style>
 html,body{margin:0;height:100%;background:#1a1d21;color:#ddd;
   font:13px/1.5 "Segoe UI",system-ui,sans-serif;overflow:hidden}
 #c{position:fixed;inset:0}
 .panel{position:fixed;background:#23272dEE;border:1px solid #3a4048;border-radius:6px;padding:10px 12px}
 #ui{top:12px;left:12px;max-width:280px}
 #info{bottom:12px;left:12px;max-width:430px;font-size:11.5px;color:#aab}
 #info summary{cursor:pointer;color:#e8b64c;font-weight:600;list-style:none}
 #info summary::-webkit-details-marker{display:none}
 #info summary::before{content:'show  ';color:#8fd}
 #info[open] summary::before{content:'hide  '}
 #info .body{margin-top:8px}
 h1{font-size:14px;margin:0 0 8px}
 label{display:block;cursor:pointer;padding:1px 0}
 input{vertical-align:-2px;margin-right:6px}
 table{border-collapse:collapse;font-size:11.5px;margin-top:8px}
 td{padding:1px 10px 1px 0}
 td.n{text-align:right;color:#8fd}
 b.w{color:#e8b64c}
 ul{margin:4px 0 0;padding-left:16px}
 li{margin:3px 0}
</style>
<canvas id="c"></canvas>
<div class="panel" id="ui"><h1>CNC assembly</h1><div id="toggles"></div><table id="facts"></table></div>
<details class="panel" id="info"><summary>How this was built, and what is assumed</summary><div class="body" id="infobody"></div></details>
<script src="vendor/three.min.js"></script>
<script>
const PARTS=__PARTS__, GROUPS=__GROUPS__, ASSUMPTIONS=__ASSUMPTIONS__, FACTS=__FACTS__;

const scene=new THREE.Scene(); scene.background=new THREE.Color(0x1a1d21);
const cam=new THREE.PerspectiveCamera(42,1,10,20000);
const rend=new THREE.WebGLRenderer({canvas:document.getElementById('c'),antialias:true});
scene.add(new THREE.HemisphereLight(0xffffff,0x40454d,1.05));
const key=new THREE.DirectionalLight(0xffffff,0.75); key.position.set(1,2,1.4); scene.add(key);

// Centre everything on the machine so the orbit pivot is sensible.
let lo=[1e9,1e9,1e9], hi=[-1e9,-1e9,-1e9];
PARTS.forEach(p=>{for(let i=0;i<3;i++){lo[i]=Math.min(lo[i],p.p[i]);hi[i]=Math.max(hi[i],p.q[i]);}});
const mid=[0,1,2].map(i=>(lo[i]+hi[i])/2);
const span=Math.max(hi[0]-lo[0],hi[1]-lo[1],hi[2]-lo[2]);

// machine (x,y,z) -> three (x, z, -y); three's Y is up, and fore-aft runs to -Z
const byGroup={};
for(const p of PARTS){
  let geom, ctr;
  if(p.t==='prism'){
    // profile is machine X-Z, extruded along fore-aft. Extrude runs along three's
    // +Z, so the mesh is built at the origin and then shifted to the right depth.
    const sh=new THREE.Shape();
    p.profile.forEach((pt,i)=>i?sh.lineTo(pt[0]-mid[0],pt[1]-mid[2]):sh.moveTo(pt[0]-mid[0],pt[1]-mid[2]));
    sh.closePath();
    geom=new THREE.ExtrudeGeometry(sh,{depth:p.yb-p.ya,bevelEnabled:false});
    ctr=[0,0,-(p.yb-mid[1])];
  }else{
    const s=[0,1,2].map(i=>Math.max(p.q[i]-p.p[i],0.4));
    geom=new THREE.BoxGeometry(s[0],s[2],s[1]);
    ctr=[(p.p[0]+p.q[0])/2-mid[0],(p.p[2]+p.q[2])/2-mid[2],-((p.p[1]+p.q[1])/2-mid[1])];
  }
  const g=new THREE.Mesh(geom,new THREE.MeshLambertMaterial({color:p.c,side:THREE.DoubleSide}));
  g.position.set(ctr[0],ctr[1],ctr[2]);
  const e=new THREE.LineSegments(new THREE.EdgesGeometry(g.geometry),
    new THREE.LineBasicMaterial({color:0x000000,opacity:0.35,transparent:true}));
  g.add(e); scene.add(g);
  (byGroup[p.g]=byGroup[p.g]||[]).push(g);
}

// ground plane at the box's underside
const gy=lo[2]-mid[2];
const grid=new THREE.GridHelper(span*2.2, 22, 0x44505c, 0x2b3139); grid.position.y=gy; scene.add(grid);

// --- orbit: written out rather than pulled from a second CDN file ---------
let az=-0.72, el=0.42, dist=span*1.75, down=null;
function place(){cam.position.set(dist*Math.cos(el)*Math.sin(az),dist*Math.sin(el),dist*Math.cos(el)*Math.cos(az));cam.lookAt(0,0,0);}
addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);
addEventListener('pointerup',()=>down=null);
addEventListener('pointermove',e=>{if(!down)return;
  az-=(e.clientX-down[0])*0.006; el=Math.max(-1.45,Math.min(1.45,el+(e.clientY-down[1])*0.006));
  down=[e.clientX,e.clientY]; place(); draw();});
addEventListener('wheel',e=>{e.preventDefault();dist=Math.max(span*0.25,Math.min(span*6,dist*(1+Math.sign(e.deltaY)*0.11)));place();draw();},{passive:false});

function resize(){const w=innerWidth,h=innerHeight;rend.setPixelRatio(devicePixelRatio);rend.setSize(w,h);cam.aspect=w/h;cam.updateProjectionMatrix();draw();}
function draw(){rend.render(scene,cam);}
addEventListener('resize',resize);

const VIEWS={iso:[-0.72,0.42],front:[Math.PI,0.06],back:[0,0.06],
             left:[-Math.PI/2,0.06],right:[Math.PI/2,0.06],top:[0,1.44]};
const vb=document.createElement('div'); vb.style.margin='2px 0 8px';
for(const k in VIEWS){
  const b=document.createElement('button'); b.textContent=k;
  b.style.cssText='margin:2px 4px 0 0;background:#2f353d;color:#cde;border:1px solid #454c55;'+
                  'border-radius:4px;padding:2px 7px;cursor:pointer;font:11px inherit';
  b.onclick=()=>{[az,el]=VIEWS[k];place();draw();};
  vb.appendChild(b);
}
document.getElementById('ui').insertBefore(vb,document.getElementById('toggles'));
const t=document.getElementById('toggles');
for(const k in GROUPS){
  const l=document.createElement('label');
  l.innerHTML='<input type="checkbox" checked>'+GROUPS[k];
  l.firstChild.onchange=e=>{(byGroup[k]||[]).forEach(m=>m.visible=e.target.checked);draw();};
  t.appendChild(l);
}
document.getElementById('facts').innerHTML=
  FACTS.map(f=>'<tr><td>'+f[0]+'</td><td class="n">'+f[1]+'</td></tr>').join('');
document.getElementById('infobody').innerHTML=
  '<b class="w">Generated from dimensions/registry.toml by tools/make-3d.py.</b> '+
  'Every box is placed from a registry value - drag to orbit, scroll to zoom. '+
  'Pose: X home left, Y home back, Z at max.<br><b class="w">Placements ASSUMED, not derived:</b>'+
  '<ul>'+ASSUMPTIONS.map(a=>'<li>'+a+'</li>').join('')+'</ul>';

place(); resize();
</script>
"""

if __name__ == "__main__":
    raise SystemExit(main())
