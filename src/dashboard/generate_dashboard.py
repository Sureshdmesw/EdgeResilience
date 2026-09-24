# -*- coding: utf-8 -*-
"""EdgeResilience Dashboard Generator â€” writes _part1_head.html, _part2_body.html, _part3_pages.html"""
from pathlib import Path
DASH = Path(__file__).resolve().parent

# â”€â”€ PART 1: HEAD + CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
P1 = []
P1.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>EdgeResilience â€” Edge AI Safety Intelligence Console</title>
<style>
:root{
  --bg:#04080f;--surface:#080f1c;--surface2:#0c1525;--surface3:#111d30;
  --border:#162035;--border2:#1e2e47;--border3:#243858;
  --text:#e2edf8;--text2:#8aa8c4;--text3:#4d6a85;--text4:#2d4a62;
  --accent:#38bdf8;--accent2:#0ea5e9;--accent-dim:rgba(56,189,248,.08);
  --good:#34d399;--good-dim:rgba(52,211,153,.08);--good-border:rgba(52,211,153,.3);
  --warn:#fbbf24;--warn-dim:rgba(251,191,36,.08);--warn-border:rgba(251,191,36,.3);
  --danger:#f87171;--danger-dim:rgba(248,113,113,.08);--danger-border:rgba(248,113,113,.3);
  --medium:#fb923c;--medium-dim:rgba(251,146,60,.08);--medium-border:rgba(251,146,60,.3);
  --purple:#a78bfa;--purple-dim:rgba(167,139,250,.08);
  --r4:4px;--r8:8px;--r12:12px;--r16:16px;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
  --mono:'JetBrains Mono','Fira Code','Cascadia Code',monospace;
  --ease:cubic-bezier(.4,0,.2,1);
  --t150:150ms;--t300:300ms;--t500:500ms;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.5;min-height:100vh;overflow-x:hidden;-webkit-font-smoothing:antialiased}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
button{font-family:var(--font);cursor:pointer}
""")
P1.append("""
/* TOPNAV */
.topnav{position:sticky;top:0;z-index:200;background:rgba(4,8,15,.94);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);height:52px;display:flex;align-items:center;padding:0 20px;gap:0}
.topnav-brand{display:flex;align-items:center;gap:10px;margin-right:24px;flex-shrink:0}
.brand-mark{width:28px;height:28px;border-radius:6px;background:linear-gradient(135deg,var(--accent2),#6366f1);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;color:#fff;flex-shrink:0}
.brand-name{font-size:15px;font-weight:800;color:var(--text);letter-spacing:-.4px}
.brand-name span{color:var(--accent)}
.topnav-tabs{display:flex;align-items:center;gap:2px;flex:1}
.tab{display:flex;align-items:center;gap:6px;padding:6px 11px;border-radius:var(--r8);font-size:12.5px;font-weight:500;color:var(--text3);cursor:pointer;border:none;background:transparent;transition:all var(--t150) var(--ease);white-space:nowrap;user-select:none}
.tab:hover{color:var(--text2);background:var(--surface2)}
.tab.active{color:var(--accent);background:var(--accent-dim);font-weight:600}
.tab-icon{font-size:13px}
.topnav-right{display:flex;align-items:center;gap:8px;flex-shrink:0;margin-left:12px}
.sys-pill{display:flex;align-items:center;gap:5px;padding:4px 10px;border-radius:20px;font-size:10.5px;font-weight:600;border:1px solid;white-space:nowrap}
.pill-good{background:var(--good-dim);border-color:var(--good-border);color:var(--good)}
.pill-warn{background:var(--warn-dim);border-color:var(--warn-border);color:var(--warn)}
.pill-dot{width:5px;height:5px;border-radius:50%;background:currentColor}
.pill-dot.pulse{animation:dot-pulse 2.5s infinite}
@keyframes dot-pulse{0%,100%{opacity:1}50%{opacity:.25}}
.mode-btn{display:flex;align-items:center;gap:5px;padding:5px 11px;border-radius:var(--r8);font-size:11px;font-weight:600;border:1px solid var(--border2);background:var(--surface2);color:var(--text2);cursor:pointer;transition:all var(--t150) var(--ease)}
.mode-btn:hover{border-color:var(--accent);color:var(--accent)}
.mode-btn.on{border-color:var(--accent);background:var(--accent-dim);color:var(--accent)}
/* SHELL */
.shell{min-height:calc(100vh - 52px)}
.page{display:none;padding:28px 24px;max-width:1400px;margin:0 auto}
.page.active{display:block}
/* GRIDS */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.g21{display:grid;grid-template-columns:2fr 1fr;gap:16px}
.g12{display:grid;grid-template-columns:1fr 2fr;gap:16px}
@media(max-width:1100px){.g3{grid-template-columns:1fr 1fr}.g4{grid-template-columns:1fr 1fr}.g21,.g12{grid-template-columns:1fr}}
@media(max-width:700px){.g2,.g3,.g4{grid-template-columns:1fr}.page{padding:16px 14px}}
""")
P1.append("""
/* CARDS */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r12);padding:18px}
.card-sm{padding:14px}
.card-hd{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.12em;margin-bottom:12px}
.card-accent{border-top:2px solid var(--accent)}
.card-good{border-top:2px solid var(--good)}
.card-warn{border-top:2px solid var(--warn)}
.card-danger{border-top:2px solid var(--danger)}
.card-medium{border-top:2px solid var(--medium)}
.card-purple{border-top:2px solid var(--purple)}
/* BADGES */
.badge{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;text-transform:uppercase;letter-spacing:.06em;border:1px solid}
.badge::before{content:'';width:4px;height:4px;border-radius:50%;background:currentColor;flex-shrink:0}
.badge-v{background:var(--good-dim);border-color:var(--good-border);color:var(--good)}
.badge-p{background:var(--warn-dim);border-color:var(--warn-border);color:var(--warn)}
.badge-d{background:var(--danger-dim);border-color:var(--danger-border);color:var(--danger)}
.badge-i{background:var(--surface2);border-color:var(--border2);color:var(--text2)}
.badge-prep{background:rgba(52,211,153,.05);border-color:rgba(52,211,153,.2);color:#6ee7b7}
.badge-fut{background:var(--purple-dim);border-color:rgba(167,139,250,.3);color:var(--purple)}
/* RISK/CONN COLORS */
.risk-NORMAL,.risk-LOW{color:var(--good)}
.risk-MEDIUM{color:var(--medium)}
.risk-HIGH{color:var(--warn)}
.risk-CRITICAL{color:var(--danger)}
.conn-CONNECTED{color:var(--good)}
.conn-DEGRADED{color:var(--warn)}
.conn-DISCONNECTED{color:var(--danger)}
/* METRIC ROW */
.mrow{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid var(--border)}
.mrow:last-child{border-bottom:none}
.mlabel{font-size:12px;color:var(--text2)}
.mval{font-size:12px;font-weight:600;font-family:var(--mono);color:var(--text)}
/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:7px;padding:9px 18px;border-radius:var(--r8);font-size:13px;font-weight:600;cursor:pointer;border:1px solid;transition:all var(--t150) var(--ease);font-family:var(--font)}
.btn-primary{background:var(--accent2);border-color:var(--accent);color:#fff}
.btn-primary:hover{background:var(--accent);color:#000;box-shadow:0 4px 16px rgba(56,189,248,.2)}
.btn-ghost{background:transparent;border-color:var(--border2);color:var(--text2)}
.btn-ghost:hover{background:var(--surface2);color:var(--text)}
.btn-sm{padding:6px 13px;font-size:12px}
.btn:disabled{opacity:.4;cursor:not-allowed}
""")
P1.append("""
/* HERO */
.hero{background:linear-gradient(135deg,var(--surface) 0%,var(--surface2) 60%,rgba(56,189,248,.04) 100%);border:1px solid var(--border);border-radius:var(--r16);padding:28px 32px;margin-bottom:20px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-60px;right:-60px;width:280px;height:280px;background:radial-gradient(circle,rgba(56,189,248,.06) 0%,transparent 70%);pointer-events:none}
.hero-eyebrow{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.16em;margin-bottom:10px}
.hero-title{font-size:32px;font-weight:900;color:var(--text);letter-spacing:-.8px;line-height:1.1}
.hero-title span{color:var(--accent)}
.hero-tagline{font-size:16px;font-weight:600;color:var(--text2);margin-top:8px;line-height:1.4;max-width:600px}
.hero-sub{font-size:12px;color:var(--text3);margin-top:6px;max-width:560px;line-height:1.6}
.hero-badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
/* SYSTEM STATE HERO */
.state-hero{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px}
@media(max-width:700px){.state-hero{grid-template-columns:1fr}}
.state-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r12);padding:16px 18px;position:relative;overflow:hidden;transition:border-color var(--t300) var(--ease)}
.state-card-eyebrow{font-size:9.5px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.14em;margin-bottom:8px}
.state-card-val{font-size:36px;font-weight:900;line-height:1;letter-spacing:-.5px;transition:color var(--t300) var(--ease),transform var(--t300) var(--ease)}
.state-card-label{font-size:11px;color:var(--text3);margin-top:5px}
.state-card-sub{font-size:10.5px;color:var(--text3);margin-top:8px;font-family:var(--mono)}
/* FLOW STRIP */
.flow-strip{display:flex;align-items:center;flex-wrap:wrap;gap:0;margin-bottom:20px}
.flow-step{display:flex;flex-direction:column;align-items:center;gap:3px;padding:10px 14px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--r8);min-width:82px;text-align:center;transition:all var(--t300) var(--ease)}
.flow-step.fs-active{border-color:var(--accent);background:var(--accent-dim)}
.flow-step.fs-good{border-color:var(--good-border);background:var(--good-dim)}
.flow-step.fs-warn{border-color:var(--warn-border);background:var(--warn-dim)}
.flow-step.fs-danger{border-color:var(--danger-border);background:var(--danger-dim)}
.fs-label{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text3)}
.fs-val{font-size:13px;font-weight:800;color:var(--text);transition:color var(--t300)}
.fs-sub{font-size:9px;color:var(--text3)}
.flow-arrow{font-size:14px;color:var(--border2);padding:0 5px;flex-shrink:0}
/* PIPELINE */
.pipeline{display:flex;flex-direction:column;gap:0}
.pipe-node{display:flex;align-items:flex-start;gap:12px;padding:10px 0;position:relative}
.pipe-node:not(:last-child)::after{content:'';position:absolute;left:14px;top:40px;width:2px;height:calc(100% - 16px);background:var(--border)}
.pipe-icon{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;z-index:1;border:2px solid var(--border2);background:var(--surface2);transition:all var(--t300) var(--ease)}
.pipe-icon.pi-active{border-color:var(--accent);background:var(--accent-dim)}
.pipe-icon.pi-good{border-color:var(--good-border);background:var(--good-dim)}
.pipe-icon.pi-warn{border-color:var(--warn-border);background:var(--warn-dim)}
.pipe-icon.pi-danger{border-color:var(--danger-border);background:var(--danger-dim)}
.pipe-body{flex:1;padding-top:3px}
.pipe-title{font-size:12.5px;font-weight:600;color:var(--text)}
.pipe-desc{font-size:11px;color:var(--text3);margin-top:2px;transition:color var(--t300)}
/* ACCORDION */
.acc-hd{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;cursor:pointer;background:var(--surface2);border:1px solid var(--border);border-radius:var(--r8);margin-bottom:3px;font-size:13px;font-weight:600;color:var(--text);user-select:none;transition:background var(--t150)}
.acc-hd:hover{background:var(--surface3)}
.acc-hd .chev{transition:transform var(--t300) var(--ease);color:var(--text3);font-size:11px}
.acc-hd.open .chev{transform:rotate(180deg)}
.acc-body{display:none;padding:16px;background:var(--surface);border:1px solid var(--border);border-top:none;border-radius:0 0 var(--r8) var(--r8);margin-bottom:8px}
.acc-body.open{display:block}
/* MISC */
.divider{height:1px;background:var(--border);margin:16px 0}
.loading{display:flex;align-items:center;gap:8px;color:var(--text3);font-size:12px;padding:20px 0}
.spinner{width:14px;height:14px;border-radius:50%;border:2px solid var(--border2);border-top-color:var(--accent);animation:spin .7s linear infinite;flex-shrink:0}
@keyframes spin{to{transform:rotate(360deg)}}
.hash-box{background:var(--surface2);border:1px solid var(--border);border-radius:var(--r8);padding:10px 14px;font-family:var(--mono);font-size:10.5px;color:var(--text3);word-break:break-all;line-height:1.7;margin-bottom:8px}
.hash-label{font-size:9px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.1em;display:block;margin-bottom:4px}
.hash-val{color:var(--accent)}
.feat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:4px}
.feat-item{background:var(--surface2);border:1px solid var(--border);border-radius:4px;padding:5px 10px;font-size:10.5px;font-family:var(--mono);color:var(--text2);display:flex;align-items:center;gap:7px}
.feat-num{font-size:9px;color:var(--text4);width:16px;text-align:right;flex-shrink:0}
.safety-bar{background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r8);padding:10px 16px;display:flex;flex-wrap:wrap;gap:16px;align-items:center}
.safety-item{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text3)}
.s-no{color:var(--danger);font-weight:700}.s-yes{color:var(--good);font-weight:700}
.roadmap-item{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid var(--border)}
.roadmap-item:last-child{border-bottom:none}
.roadmap-num{width:24px;height:24px;border-radius:50%;background:var(--surface2);border:1px solid var(--border2);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:var(--text3);flex-shrink:0;margin-top:2px}
.roadmap-title{font-size:13px;font-weight:600;color:var(--text)}
.roadmap-sub{font-size:11.5px;color:var(--text3);margin-top:3px}
/* DEPLOY JOURNEY */
.dstep{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid var(--border);position:relative}
.dstep:last-child{border-bottom:none}
.dstep:not(:last-child)::after{content:'';position:absolute;left:11px;top:38px;width:2px;height:calc(100% - 14px);background:var(--border)}
.dnum{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;flex-shrink:0;z-index:1}
.dn-done{background:var(--good-dim);border:2px solid var(--good-border);color:var(--good)}
.dn-prep{background:rgba(52,211,153,.04);border:2px solid rgba(52,211,153,.2);color:#6ee7b7}
.dn-pend{background:var(--warn-dim);border:2px solid var(--warn-border);color:var(--warn);opacity:.7}
.dn-fut{background:var(--surface2);border:2px solid var(--border2);color:var(--text3);opacity:.5}
.dbody{flex:1}
.dtitle{font-size:13px;font-weight:600;color:var(--text)}
.dsub{font-size:11.5px;color:var(--text3);margin-top:2px}
/* CYCLE CARD */
.cycle-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r12);padding:14px;transition:border-color var(--t300) var(--ease),box-shadow var(--t300) var(--ease);margin-bottom:10px}
.cycle-card:last-child{margin-bottom:0}
.cycle-card.cc-active{border-color:var(--accent);box-shadow:0 0 0 1px rgba(56,189,248,.12),0 4px 20px rgba(56,189,248,.06)}
.cc-hd{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.cc-id{font-size:11px;font-weight:700;font-family:var(--mono);color:var(--accent)}
.cc-label{font-size:11px;color:var(--text2)}
.cc-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}
.ctag{display:flex;flex-direction:column;gap:1px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--r4);padding:5px 9px;min-width:76px}
.ctag-l{font-size:8.5px;color:var(--text3);text-transform:uppercase;letter-spacing:.07em}
.ctag-v{font-size:11.5px;font-weight:700}
.ctag-yes{color:var(--good)}.ctag-no{color:var(--text3)}
/* DEG BAR */
.deg-wrap{margin:8px 0 4px}
.deg-labels{display:flex;justify-content:space-between;font-size:10.5px;color:var(--text3);margin-bottom:4px}
.deg-labels strong{color:var(--text);font-family:var(--mono)}
.deg-bg{height:5px;background:var(--surface3);border-radius:3px;overflow:hidden}
.deg-fill{height:5px;border-radius:3px;transition:width .6s var(--ease)}
/* CONN FLOW */
.conn-flow{display:flex;align-items:stretch;gap:0;overflow-x:auto;padding:4px 0}
.conn-stage{display:flex;flex-direction:column;align-items:center;gap:5px;min-width:90px;padding:12px 8px;border-radius:var(--r8);background:var(--surface2);border:1px solid var(--border);text-align:center;transition:all var(--t300) var(--ease)}
.conn-stage.cs-active{border-color:var(--accent);background:var(--accent-dim)}
.conn-stage.cs-good{border-color:var(--good-border);background:var(--good-dim)}
.conn-stage.cs-warn{border-color:var(--warn-border);background:var(--warn-dim)}
.conn-stage.cs-danger{border-color:var(--danger-border);background:var(--danger-dim)}
.cs-icon{font-size:18px}
.cs-label{font-size:9.5px;font-weight:700;color:var(--text);text-transform:uppercase;letter-spacing:.05em}
.cs-sub{font-size:8.5px;color:var(--text3)}
.conn-arrow{font-size:14px;color:var(--border2);padding:0 4px;flex-shrink:0;align-self:center}
/* TRUST LAYER */
.trust-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border)}
.trust-row:last-child{border-bottom:none}
.trust-name{font-size:12.5px;color:var(--text)}
.trust-detail{font-size:10.5px;color:var(--text3);font-family:var(--mono);margin-top:1px}
/* TEMPORAL VIZ */
.temporal-wrap{position:relative;margin:8px 0}
.temporal-svg{width:100%;height:80px;display:block}
/* ABLATION */
.abl-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border)}
.abl-row:last-child{border-bottom:none}
.abl-label{font-size:11.5px;color:var(--text2);flex:1}
.abl-bar-wrap{width:120px;height:7px;background:var(--surface3);border-radius:4px;overflow:hidden;flex-shrink:0}
.abl-bar{height:7px;border-radius:4px}
.abl-val{font-size:11px;font-family:var(--mono);color:var(--text);width:52px;text-align:right;flex-shrink:0}
.abl-best{color:var(--good)}
/* PROV TABLE */
.prov-row{display:grid;grid-template-columns:1fr 130px 110px;gap:8px;align-items:center;padding:9px 12px;border-bottom:1px solid var(--border);font-size:11px}
.prov-row:last-child{border-bottom:none}
.prov-hd{background:var(--surface2);font-size:9px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.08em;border-radius:var(--r4) var(--r4) 0 0}
.prov-name{color:var(--text);font-family:var(--mono)}
.prov-class{color:var(--text3)}
/* DEMO CONTROLS */
.demo-controls{display:flex;align-items:center;gap:10px;margin-bottom:20px;flex-wrap:wrap}
.demo-step-info{font-size:12px;color:var(--text3)}
/* STATE MACHINE */
.sm-wrap{display:flex;flex-direction:column;gap:0}
.sm-node{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid var(--border);position:relative;transition:all var(--t300) var(--ease)}
.sm-node:last-child{border-bottom:none}
.sm-node:not(:last-child)::after{content:'';position:absolute;left:15px;top:42px;width:2px;height:calc(100% - 18px);background:var(--border)}
.sm-dot{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;z-index:1;border:2px solid var(--border2);background:var(--surface2);transition:all var(--t300) var(--ease)}
.sm-dot.sm-active{border-color:var(--accent);background:var(--accent-dim);box-shadow:0 0 12px rgba(56,189,248,.2)}
.sm-dot.sm-done{border-color:var(--good-border);background:var(--good-dim)}
.sm-body{flex:1}
.sm-title{font-size:13px;font-weight:700;color:var(--text)}
.sm-desc{font-size:11.5px;color:var(--text3);margin-top:3px}
.sm-activity{font-size:11px;color:var(--text2);margin-top:4px;font-style:italic}
/* ANIMATIONS */
@keyframes fade-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes num-pop{0%{transform:scale(1)}40%{transform:scale(1.1)}100%{transform:scale(1)}}
.anim-in{animation:fade-in var(--t300) var(--ease) both}
/* REDUCED MOTION */
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;transition-duration:.01ms!important}}
/* MOBILE */
@media(max-width:768px){
  .topnav-right .sys-pill{display:none}
  .brand-name{font-size:13px}
  .hero{padding:20px 18px}
  .hero-title{font-size:24px}
}
@media(max-width:520px){
  .tab{padding:6px 8px;font-size:11px}
  .tab .tab-label{display:none}
}
</style>
</head>
<body>
""")

# Write part 1
(DASH / "_part1_head.html").write_text("".join(P1), encoding="utf-8")
print("part1 written:", len("".join(P1)), "chars")

# â”€â”€ PART 2: BODY / TOPNAV / COMMAND CENTER / LIVE DEMO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
P2 = []
P2.append("""<div class="topnav" role="banner">
  <div class="topnav-brand">
    <div class="brand-mark">ER</div>
    <div class="brand-name"><span>Edge</span>Resilience</div>
  </div>
  <div class="topnav-tabs" role="navigation" aria-label="Main navigation">
    <button class="tab active" onclick="showPage('cmd')" id="nav-cmd" aria-label="Command Center">
      <span class="tab-icon">&#9635;</span><span class="tab-label">Command Center</span>
    </button>
    <button class="tab" onclick="showPage('demo')" id="nav-demo" aria-label="Live Demo">
      <span class="tab-icon">&#9654;</span><span class="tab-label">Live Demo</span>
    </button>
    <button class="tab" onclick="showPage('ai')" id="nav-ai" aria-label="AI Intelligence">
      <span class="tab-icon">&#9672;</span><span class="tab-label">Intelligence</span>
    </button>
    <button class="tab" onclick="showPage('resilience')" id="nav-resilience" aria-label="Resilience">
      <span class="tab-icon">&#8635;</span><span class="tab-label">Resilience</span>
    </button>
    <button class="tab" onclick="showPage('evidence')" id="nav-evidence" aria-label="Evidence">
      <span class="tab-icon">&#8801;</span><span class="tab-label">Evidence</span>
    </button>
    <button class="tab" onclick="showPage('deploy')" id="nav-deploy" aria-label="Deployment">
      <span class="tab-icon">&#9678;</span><span class="tab-label">Deployment</span>
    </button>
    <button class="tab" onclick="showPage('system')" id="nav-system" aria-label="System">
      <span class="tab-icon">&#9636;</span><span class="tab-label">System</span>
    </button>
  </div>
  <div class="topnav-right">
    <div class="sys-pill pill-good"><span class="pill-dot pulse"></span>LOCAL INFERENCE ACTIVE</div>
    <div class="sys-pill pill-warn"><span class="pill-dot"></span>SNAPDRAGON PENDING</div>
    <button class="mode-btn" id="pres-btn" onclick="togglePresMode()" aria-label="Toggle presentation mode">&#9654; Present</button>
  </div>
</div>
<div class="shell">
""")
P2.append("""
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: COMMAND CENTER                                            -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page active" id="page-cmd">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-eyebrow">Qualcomm Snapdragon AI Lab Build and Present Challenge</div>
    <div class="hero-title"><span>Edge</span>Resilience</div>
    <div class="hero-tagline">Snapdragon-Powered Predictive Intelligence for Connected Vehicle Safety</div>
    <div class="hero-sub">V4 Temporal Transformer &middot; 17 features &times; 12 steps &middot; local edge inference &middot; connectivity resilience &middot; tamper-evident evidence</div>
    <div class="hero-badges" id="cmd-hero-badges">
      <div class="loading"><div class="spinner"></div>Loading system state&hellip;</div>
    </div>
  </div>

  <!-- SYSTEM STATE â€” 3 dominant cards -->
  <div class="state-hero" id="cmd-state-hero">
    <div class="state-card card-accent" id="sc-predict">
      <div class="state-card-eyebrow">&#9672; AI Prediction</div>
      <div class="state-card-val" id="sc-deg-val" style="color:var(--accent)">&mdash;</div>
      <div class="state-card-label">future_degradation</div>
      <div class="state-card-sub" id="sc-risk-val">&mdash;</div>
      <div style="font-size:9.5px;color:var(--text4);margin-top:6px;font-family:var(--mono)">V4_DEGRADATION_DEMO_POLICY_V1</div>
    </div>
    <div class="state-card card-good" id="sc-conn">
      <div class="state-card-eyebrow">&#8635; Connectivity</div>
      <div class="state-card-val" id="sc-conn-val" style="color:var(--good)">&mdash;</div>
      <div class="state-card-label">connectivity state</div>
      <div style="margin-top:10px;display:flex;flex-direction:column;gap:4px">
        <div style="display:flex;justify-content:space-between;font-size:11px">
          <span style="color:var(--text3)">Local inference</span>
          <span style="color:var(--good);font-weight:700">ALWAYS ACTIVE</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:11px">
          <span style="color:var(--text3)">Evidence records</span>
          <span style="font-weight:700;font-family:var(--mono)" id="sc-evcount">&mdash;</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:11px">
          <span style="color:var(--text3)">Sync status</span>
          <span style="font-weight:700" id="sc-sync">&mdash;</span>
        </div>
      </div>
    </div>
    <div class="state-card card-purple" id="sc-trust">
      <div class="state-card-eyebrow">&#10003; Validation</div>
      <div style="display:flex;flex-direction:column;gap:6px;margin-top:4px">
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:11.5px">
          <span style="color:var(--text2)">CPU reference</span>
          <span class="badge badge-v">VERIFIED</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:11.5px">
          <span style="color:var(--text2)">ONNX runtime</span>
          <span class="badge badge-v">VERIFIED</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:11.5px">
          <span style="color:var(--text2)">Test MAE</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--good);font-weight:700">0.0051</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:11.5px">
          <span style="color:var(--text2)">ONNX speedup</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--accent);font-weight:700">~5.99&times; CPU</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:11.5px">
          <span style="color:var(--text2)">Snapdragon HW</span>
          <span class="badge badge-p">NOT VERIFIED</span>
        </div>
      </div>
    </div>
  </div>

  <!-- PIPELINE FLOW STRIP -->
  <div style="margin-bottom:20px">
    <div style="font-size:9.5px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.14em;margin-bottom:10px">Edge AI Pipeline</div>
    <div class="flow-strip" id="cmd-flow">
      <div class="flow-step fs-active">
        <span class="fs-label">Observe</span>
        <span class="fs-val">17&times;12</span>
        <span class="fs-sub">cyber features</span>
      </div>
      <div class="flow-arrow">&#8594;</div>
      <div class="flow-step fs-active">
        <span class="fs-label">Predict</span>
        <span class="fs-val" id="fs-predict">&mdash;</span>
        <span class="fs-sub">future_degradation</span>
      </div>
      <div class="flow-arrow">&#8594;</div>
      <div class="flow-step" id="fs-assess-step">
        <span class="fs-label">Assess</span>
        <span class="fs-val" id="fs-risk">&mdash;</span>
        <span class="fs-sub">risk level</span>
      </div>
      <div class="flow-arrow">&#8594;</div>
      <div class="flow-step fs-good">
        <span class="fs-label">Resilience</span>
        <span class="fs-val" style="color:var(--good);font-size:11px">LOCAL</span>
        <span class="fs-sub">always active</span>
      </div>
      <div class="flow-arrow">&#8594;</div>
      <div class="flow-step" id="fs-preserve-step">
        <span class="fs-label">Preserve</span>
        <span class="fs-val" id="fs-buf">&mdash;</span>
        <span class="fs-sub">evidence records</span>
      </div>
      <div class="flow-arrow">&#8594;</div>
      <div class="flow-step" id="fs-recover-step">
        <span class="fs-label">Recover</span>
        <span class="fs-val" id="fs-sync">&mdash;</span>
        <span class="fs-sub">sync state</span>
      </div>
    </div>
  </div>

  <!-- SCENARIO TIMELINE + QUICK STATS -->
  <div class="g21" style="margin-bottom:20px">
    <div class="card">
      <div class="card-hd">Three-Cycle Scenario &mdash; <span style="color:var(--text2);font-weight:400;text-transform:none">Connected &rarr; Disconnected &rarr; Recovery</span></div>
      <div id="cmd-timeline"><div class="loading"><div class="spinner"></div>Loading&hellip;</div></div>
    </div>
    <div class="card">
      <div class="card-hd">System Intelligence</div>
      <div class="mrow"><span class="mlabel">Model</span><span class="mval" style="color:var(--accent);font-size:10.5px">V4 Temporal Predictor</span></div>
      <div class="mrow"><span class="mlabel">Parameters</span><span class="mval">71,170</span></div>
      <div class="mrow"><span class="mlabel">Input window</span><span class="mval">12 steps &times; 17 features</span></div>
      <div class="mrow"><span class="mlabel">Test MAE</span><span class="mval" style="color:var(--good)">0.0051</span></div>
      <div class="mrow"><span class="mlabel">Test RMSE</span><span class="mval" style="color:var(--good)">0.0066</span></div>
      <div class="mrow"><span class="mlabel">ONNX max error</span><span class="mval" style="color:var(--good)">5.96e-08</span></div>
      <div class="mrow"><span class="mlabel">ONNX speedup</span><span class="mval" style="color:var(--accent)">~5.99&times; CPU-to-CPU</span></div>
      <div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border)">
        <div style="font-size:9.5px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px">Deployment Status</div>
        <div style="display:flex;flex-direction:column;gap:5px">
          <div style="display:flex;justify-content:space-between;font-size:11.5px"><span style="color:var(--text2)">CPU reference</span><span class="badge badge-v">VERIFIED</span></div>
          <div style="display:flex;justify-content:space-between;font-size:11.5px"><span style="color:var(--text2)">ONNX Runtime</span><span class="badge badge-v">VERIFIED</span></div>
          <div style="display:flex;justify-content:space-between;font-size:11.5px"><span style="color:var(--text2)">Snapdragon HW</span><span class="badge badge-p">NOT VERIFIED</span></div>
          <div style="display:flex;justify-content:space-between;font-size:11.5px"><span style="color:var(--text2)">QNN / NPU</span><span class="badge badge-p">NOT VERIFIED</span></div>
        </div>
      </div>
    </div>
  </div>

  <!-- SAFETY BOUNDARY -->
  <div class="safety-bar">
    <span style="font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.1em">Safety Boundary</span>
    <div class="safety-item">Physical vehicle: <span class="s-no">NO</span></div>
    <div class="safety-item">External CAN: <span class="s-no">NO</span></div>
    <div class="safety-item">Direct actuation: <span class="s-no">NO</span></div>
    <div class="safety-item">Production vehicle: <span class="s-no">NO</span></div>
    <div class="safety-item">Classification: <span class="s-yes">SOFTWARE SIMULATION / VIRTUAL LAB</span></div>
  </div>
</div>
""")
P2.append("""
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: LIVE DEMO                                                 -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page" id="page-demo">
  <div class="sec-hd">
    <div class="sec-eyebrow">Interactive Demonstration</div>
    <div class="sec-title">EdgeResilience Lifecycle</div>
    <div class="sec-sub">Step through the deterministic three-cycle scenario &mdash; all values from validated V4 runtime</div>
  </div>

  <!-- DEMO CONTROLS -->
  <div class="demo-controls">
    <button class="btn btn-primary" onclick="stepDemo()" id="btn-step" aria-label="Advance to next cycle">&#9654; Next Cycle</button>
    <button class="btn btn-ghost btn-sm" onclick="autoPlay()" id="btn-auto" aria-label="Auto play demo">&#9654;&#9654; Auto Play</button>
    <button class="btn btn-ghost btn-sm" onclick="resetDemo()" aria-label="Reset demo">&#8635; Reset</button>
    <span class="demo-step-info" id="demo-step-label" aria-live="polite">Press <strong style="color:var(--accent)">Next Cycle</strong> to begin</span>
  </div>

  <!-- WOW MOMENT: LIFECYCLE ORCHESTRATION -->
  <div class="g12" style="margin-bottom:16px">
    <!-- STATE MACHINE -->
    <div class="card">
      <div class="card-hd">Resilience State Machine</div>
      <div class="sm-wrap" id="demo-sm">
        <div class="sm-node" id="sm-observe">
          <div class="sm-dot" id="sm-dot-observe">&#128225;</div>
          <div class="sm-body">
            <div class="sm-title">Observe</div>
            <div class="sm-desc">17 cyber features &times; 12 temporal steps</div>
            <div class="sm-activity" id="sm-act-observe"></div>
          </div>
        </div>
        <div class="sm-node" id="sm-predict">
          <div class="sm-dot" id="sm-dot-predict">&#9672;</div>
          <div class="sm-body">
            <div class="sm-title">Predict</div>
            <div class="sm-desc">V4 Temporal Transformer inference</div>
            <div class="sm-activity" id="sm-act-predict"></div>
          </div>
        </div>
        <div class="sm-node" id="sm-assess">
          <div class="sm-dot" id="sm-dot-assess">&#9673;</div>
          <div class="sm-body">
            <div class="sm-title">Assess</div>
            <div class="sm-desc">Deterministic risk interpretation</div>
            <div class="sm-activity" id="sm-act-assess"></div>
          </div>
        </div>
        <div class="sm-node" id="sm-respond">
          <div class="sm-dot" id="sm-dot-respond">&#8635;</div>
          <div class="sm-body">
            <div class="sm-title">Respond</div>
            <div class="sm-desc">Connectivity evaluation &amp; local resilience</div>
            <div class="sm-activity" id="sm-act-respond"></div>
          </div>
        </div>
        <div class="sm-node" id="sm-preserve">
          <div class="sm-dot" id="sm-dot-preserve">&#8801;</div>
          <div class="sm-body">
            <div class="sm-title">Preserve</div>
            <div class="sm-desc">SHA-256 evidence buffering</div>
            <div class="sm-activity" id="sm-act-preserve"></div>
          </div>
        </div>
        <div class="sm-node" id="sm-recover">
          <div class="sm-dot" id="sm-dot-recover">&#8593;</div>
          <div class="sm-body">
            <div class="sm-title">Recover</div>
            <div class="sm-desc">Recovery detection &amp; sync manifest</div>
            <div class="sm-activity" id="sm-act-recover"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ACTIVE CYCLE SPOTLIGHT -->
    <div>
      <div class="card" style="margin-bottom:14px" id="demo-spotlight">
        <div class="card-hd">Active Cycle</div>
        <div style="color:var(--text3);font-size:12.5px">Press <strong style="color:var(--accent)">Next Cycle</strong> to begin the demonstration.</div>
      </div>

      <!-- STATE TRANSITION -->
      <div id="demo-transition" style="display:none;margin-bottom:14px">
        <div style="font-size:9.5px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px">State Transition</div>
        <div style="display:grid;grid-template-columns:1fr 32px 1fr;align-items:center">
          <div id="demo-prev-state" style="background:var(--surface2);border:1px solid var(--border);border-radius:var(--r8) 0 0 var(--r8);padding:12px 14px"></div>
          <div style="background:var(--surface2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:center;height:100%;font-size:16px;color:var(--accent)">&#8594;</div>
          <div id="demo-curr-state" style="background:var(--accent-dim);border:1px solid var(--accent);border-radius:0 var(--r8) var(--r8) 0;padding:12px 14px"></div>
        </div>
      </div>

      <!-- ALL CYCLES -->
      <div class="card">
        <div class="card-hd">All Cycles</div>
        <div id="demo-all-cycles"><div class="loading"><div class="spinner"></div>Loading&hellip;</div></div>
      </div>
    </div>
  </div>

  <!-- DEMO CONCLUSION (shown after all cycles) -->
  <div id="demo-conclusion" style="display:none">
    <div style="background:linear-gradient(135deg,rgba(52,211,153,.06),rgba(56,189,248,.06));border:1px solid var(--good-border);border-radius:var(--r12);padding:22px 26px;text-align:center">
      <div style="font-size:22px;margin-bottom:12px">&#10003;</div>
      <div style="font-size:16px;font-weight:800;color:var(--good);margin-bottom:12px">Demonstration Complete</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;max-width:700px;margin:0 auto">
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r8);padding:12px;font-size:12px;color:var(--text2)">&#9672; Prediction continued through all connectivity states</div>
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r8);padding:12px;font-size:12px;color:var(--text2)">&#8635; Local resilience remained active during disconnection</div>
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r8);padding:12px;font-size:12px;color:var(--text2)">&#8801; Evidence was preserved with SHA-256 integrity</div>
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r8);padding:12px;font-size:12px;color:var(--text2)">&#8593; Synchronization manifest became ready on recovery</div>
      </div>
    </div>
  </div>
</div>
""")

# Write part 2
(DASH / "_part2_body.html").write_text("".join(P2), encoding="utf-8")
print("part2 written:", len("".join(P2)), "chars")

# â”€â”€ PART 3: REMAINING PAGES + JS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
P3 = []
P3.append("""
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: AI INTELLIGENCE                                           -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page" id="page-ai">
  <div class="sec-hd">
    <div class="sec-eyebrow">Predictive AI</div>
    <div class="sec-title">V4 Temporal Predictor</div>
    <div class="sec-sub">EdgeResilienceTemporalPredictor &middot; 71,170 parameters &middot; VALIDATED on CPU + ONNX</div>
  </div>

  <!-- KEY METRICS -->
  <div class="g4" style="margin-bottom:16px">
    <div class="card card-good">
      <div class="card-hd">Test MAE</div>
      <div style="font-size:32px;font-weight:900;color:var(--good);line-height:1">0.0051</div>
      <div style="font-size:11px;color:var(--text3);margin-top:5px">baseline 0.0203</div>
    </div>
    <div class="card card-good">
      <div class="card-hd">Test RMSE</div>
      <div style="font-size:32px;font-weight:900;color:var(--good);line-height:1">0.0066</div>
      <div style="font-size:11px;color:var(--text3);margin-top:5px">baseline 0.0232</div>
    </div>
    <div class="card card-accent">
      <div class="card-hd">Parameters</div>
      <div style="font-size:32px;font-weight:900;color:var(--accent);line-height:1">71,170</div>
      <div style="font-size:11px;color:var(--text3);margin-top:5px">compact edge model</div>
    </div>
    <div class="card">
      <div class="card-hd">Best Epoch</div>
      <div style="font-size:32px;font-weight:900;line-height:1">77<span style="font-size:16px;color:var(--text3)">/80</span></div>
      <div style="font-size:11px;color:var(--text3);margin-top:5px">val loss 4.38e-05</div>
    </div>
  </div>

  <div class="g2" style="margin-bottom:16px">
    <!-- TEMPORAL VISUALIZATION -->
    <div class="card">
      <div class="card-hd">Temporal Intelligence &mdash; Observed History &rarr; Predicted Future</div>
      <div style="font-size:11.5px;color:var(--text3);margin-bottom:12px;line-height:1.6">The model attends to all 12 observation steps simultaneously via learned temporal attention weights. The full sequence outperforms single-step and compact representations.</div>
      <div class="temporal-wrap">
        <svg class="temporal-svg" id="ai-temporal-svg" viewBox="0 0 400 80" preserveAspectRatio="none" aria-label="Temporal observation window visualization">
          <!-- rendered by JS -->
        </svg>
        <div style="display:flex;justify-content:space-between;font-size:9.5px;color:var(--text3);margin-top:4px">
          <span>&#8592; step 1 (oldest)</span>
          <span style="color:var(--text2);font-weight:600">12 OBSERVED STEPS</span>
          <span style="color:var(--warn)">PREDICTED &#8594;</span>
        </div>
      </div>
      <div style="margin-top:14px">
        <div class="card-hd">Inference Flow</div>
        <div style="display:flex;flex-direction:column;gap:3px;align-items:center">
          <div style="width:100%;background:var(--accent-dim);border:1px solid rgba(56,189,248,.2);border-radius:var(--r8);padding:9px 14px;text-align:center">
            <div style="font-size:12px;font-weight:700;color:var(--accent)">17 features &times; 12 steps</div>
            <div style="font-size:10px;color:var(--text3)">cyber telemetry observations</div>
          </div>
          <div style="font-size:16px;color:var(--accent)">&#8595;</div>
          <div style="width:100%;background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r8);padding:9px 14px;text-align:center">
            <div style="font-size:12px;font-weight:700;color:var(--text)">Temporal Transformer</div>
            <div style="font-size:10px;color:var(--text3)">2 layers &middot; 4 heads &middot; d_model=64 &middot; attention pooling</div>
          </div>
          <div style="font-size:16px;color:var(--accent)">&#8595;</div>
          <div style="width:100%;background:var(--accent-dim);border:1px solid rgba(56,189,248,.2);border-radius:var(--r8);padding:9px 14px;text-align:center">
            <div style="font-size:12px;font-weight:700;color:var(--accent)">future_degradation</div>
            <div style="font-size:10px;color:var(--text3)">scalar [0,1] &middot; Sigmoid output</div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODEL ARCHITECTURE + ABLATION -->
    <div>
      <div class="card" style="margin-bottom:14px">
        <div class="card-hd">Model Architecture</div>
        <div class="mrow"><span class="mlabel">Type</span><span class="mval">Temporal Transformer</span></div>
        <div class="mrow"><span class="mlabel">Input projection</span><span class="mval">Linear(17 &rarr; 64)</span></div>
        <div class="mrow"><span class="mlabel">Positional embedding</span><span class="mval">Learned [1,12,64]</span></div>
        <div class="mrow"><span class="mlabel">Transformer layers</span><span class="mval">2</span></div>
        <div class="mrow"><span class="mlabel">Attention heads</span><span class="mval">4</span></div>
        <div class="mrow"><span class="mlabel">d_model</span><span class="mval">64</span></div>
        <div class="mrow"><span class="mlabel">Feed-forward dim</span><span class="mval">128</span></div>
        <div class="mrow"><span class="mlabel">Pooling</span><span class="mval">Temporal attention</span></div>
        <div class="mrow"><span class="mlabel">Output activation</span><span class="mval">Sigmoid &rarr; [0,1]</span></div>
        <div class="mrow"><span class="mlabel">Target</span><span class="mval" style="color:var(--accent)">future_degradation</span></div>
      </div>
      <div class="card">
        <div class="card-hd">Temporal Ablation &mdash; Why 12 Steps Matter</div>
        <div style="font-size:11px;color:var(--text3);margin-bottom:10px">Lower MAE = better prediction. Full sequence is the strongest neural configuration.</div>
        <div id="ai-ablation"></div>
        <div style="margin-top:8px;font-size:10px;color:var(--text3)">Synthetic V4 data only &mdash; not physical vehicle validation &mdash; Snapdragon hardware not measured</div>
      </div>
    </div>
  </div>

  <!-- TRAINING CONFIG -->
  <div class="card">
    <div class="card-hd">Training Configuration</div>
    <div class="g3">
      <div>
        <div class="mrow"><span class="mlabel">Optimizer</span><span class="mval">AdamW</span></div>
        <div class="mrow"><span class="mlabel">Learning rate</span><span class="mval">0.001</span></div>
        <div class="mrow"><span class="mlabel">Weight decay</span><span class="mval">0.0001</span></div>
        <div class="mrow"><span class="mlabel">Batch size</span><span class="mval">128</span></div>
      </div>
      <div>
        <div class="mrow"><span class="mlabel">Max epochs</span><span class="mval">80</span></div>
        <div class="mrow"><span class="mlabel">Best epoch</span><span class="mval">77</span></div>
        <div class="mrow"><span class="mlabel">Seed</span><span class="mval">42</span></div>
        <div class="mrow"><span class="mlabel">Device</span><span class="mval">CPU</span></div>
      </div>
      <div>
        <div class="mrow"><span class="mlabel">Train samples</span><span class="mval">3,200</span></div>
        <div class="mrow"><span class="mlabel">Val samples</span><span class="mval">800</span></div>
        <div class="mrow"><span class="mlabel">Test samples</span><span class="mval">1,000</span></div>
        <div class="mrow"><span class="mlabel">Dataset records</span><span class="mval">5,000</span></div>
      </div>
    </div>
  </div>
</div>
""")
P3.append("""
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: RESILIENCE                                                -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page" id="page-resilience">
  <div class="sec-hd">
    <div class="sec-eyebrow">Connectivity-Aware Resilience</div>
    <div class="sec-title">Local Intelligence. Always Active.</div>
    <div class="sec-sub">The V4 Temporal Predictor runs on-device. No cloud dependency for inference.</div>
  </div>

  <!-- HERO MESSAGE -->
  <div style="background:linear-gradient(135deg,rgba(52,211,153,.07),rgba(52,211,153,.03));border:1px solid var(--good-border);border-radius:var(--r12);padding:18px 22px;margin-bottom:20px;display:flex;align-items:center;gap:16px">
    <div style="font-size:28px;flex-shrink:0">&#9672;</div>
    <div>
      <div style="font-size:15px;font-weight:800;color:var(--good);letter-spacing:-.2px">LOCAL INTELLIGENCE CONTINUES DURING CONNECTIVITY DEGRADATION</div>
      <div style="font-size:12px;color:var(--text3);margin-top:4px">Evidence is buffered locally with SHA-256 integrity and synchronized when connectivity recovers. No cloud dependency for inference.</div>
    </div>
  </div>

  <!-- RESILIENCE LIFECYCLE FLOW -->
  <div class="card" style="margin-bottom:16px">
    <div class="card-hd">Resilience Lifecycle &mdash; Three-Cycle Demonstration</div>
    <div class="conn-flow">
      <div class="conn-stage cs-good"><div class="cs-icon">&#128994;</div><div class="cs-label">Connected</div><div class="cs-sub">cycle-001</div></div>
      <div class="conn-arrow">&#8594;</div>
      <div class="conn-stage cs-active"><div class="cs-icon">&#9672;</div><div class="cs-label">Local Inference</div><div class="cs-sub">always active</div></div>
      <div class="conn-arrow">&#8594;</div>
      <div class="conn-stage" style="border-color:var(--danger-border);background:var(--danger-dim)"><div class="cs-icon">&#128308;</div><div class="cs-label">Disconnected</div><div class="cs-sub">cycle-002</div></div>
      <div class="conn-arrow">&#8594;</div>
      <div class="conn-stage cs-warn"><div class="cs-icon">&#8801;</div><div class="cs-label">Buffering</div><div class="cs-sub">evidence preserved</div></div>
      <div class="conn-arrow">&#8594;</div>
      <div class="conn-stage cs-good"><div class="cs-icon">&#128994;</div><div class="cs-label">Recovered</div><div class="cs-sub">cycle-003</div></div>
      <div class="conn-arrow">&#8594;</div>
      <div class="conn-stage cs-active"><div class="cs-icon">&#8593;</div><div class="cs-label">Sync Ready</div><div class="cs-sub">manifest prepared</div></div>
    </div>
  </div>

  <div class="g2" style="margin-bottom:16px">
    <!-- RISK POLICY -->
    <div class="card">
      <div class="card-hd">Risk Threshold Map &mdash; V4_DEGRADATION_DEMO_POLICY_V1</div>
      <div style="background:var(--warn-dim);border:1px solid var(--warn-border);border-radius:var(--r8);padding:10px 14px;margin-bottom:12px;font-size:11.5px;color:var(--text2)">
        <strong style="color:var(--warn)">Demonstration policy only.</strong> Fixed thresholds. NOT a certified vehicle safety policy. NOT learned from data. NOT Snapdragon hardware limits.
      </div>
      <div style="display:flex;flex-direction:column;gap:6px">
        <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--good)">
          <span style="font-weight:700;color:var(--good);width:72px;font-size:12px">NORMAL</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">&lt; 0.02</span>
          <span style="margin-left:auto;font-size:10px;color:var(--text3)">no evidence</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--good)">
          <span style="font-weight:700;color:var(--good);width:72px;font-size:12px">LOW</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">0.02 &ndash; 0.04</span>
          <span style="margin-left:auto;font-size:10px;color:var(--text3)">no evidence</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--medium)">
          <span style="font-weight:700;color:var(--medium);width:72px;font-size:12px">MEDIUM</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">0.04 &ndash; 0.06</span>
          <span style="margin-left:auto;font-size:10px;color:var(--medium)">evidence required</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--warn)">
          <span style="font-weight:700;color:var(--warn);width:72px;font-size:12px">HIGH</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">0.06 &ndash; 0.07</span>
          <span style="margin-left:auto;font-size:10px;color:var(--warn)">evidence required</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--danger)">
          <span style="font-weight:700;color:var(--danger);width:72px;font-size:12px">CRITICAL</span>
          <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">&ge; 0.07</span>
          <span style="margin-left:auto;font-size:10px;color:var(--danger)">evidence required</span>
        </div>
      </div>
    </div>

    <!-- CONNECTIVITY RULES + DEMO CYCLES -->
    <div>
      <div class="card" style="margin-bottom:14px">
        <div class="card-hd">Connectivity Classification</div>
        <div style="display:flex;flex-direction:column;gap:6px">
          <div style="padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--danger)">
            <div style="font-weight:700;color:var(--danger);font-size:12px">DISCONNECTED</div>
            <div style="font-size:11px;color:var(--text3);margin-top:3px;font-family:var(--mono)">heartbeat_failure = true OR packet_loss &ge; 80%</div>
          </div>
          <div style="padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--warn)">
            <div style="font-weight:700;color:var(--warn);font-size:12px">DEGRADED</div>
            <div style="font-size:11px;color:var(--text3);margin-top:3px;font-family:var(--mono)">packet_loss &ge; 20% OR latency &ge; 250ms</div>
          </div>
          <div style="padding:9px 12px;background:var(--surface2);border-radius:var(--r8);border-left:3px solid var(--good)">
            <div style="font-weight:700;color:var(--good);font-size:12px">CONNECTED</div>
            <div style="font-size:11px;color:var(--text3);margin-top:3px;font-family:var(--mono)">otherwise</div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-hd">Demo Cycle Connectivity</div>
        <div id="res-conn-cycles"><div class="loading"><div class="spinner"></div>Loading&hellip;</div></div>
      </div>
    </div>
  </div>

  <!-- AI / DETERMINISTIC SEPARATION -->
  <div class="card" style="margin-bottom:16px">
    <div class="card-hd">AI Inference vs Deterministic Policy &mdash; Explicit Separation</div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:4px">
      <div style="flex:1;min-width:160px;background:var(--accent-dim);border:1px solid rgba(56,189,248,.2);border-radius:var(--r8);padding:14px">
        <div style="font-size:11px;font-weight:700;color:var(--accent)">AI INFERENCE LAYER</div>
        <div style="font-size:10.5px;color:var(--text3);margin-top:6px">EdgeResilienceTemporalPredictor</div>
        <div style="font-size:10.5px;color:var(--text3)">&rarr; predicted_future_degradation</div>
        <div style="font-size:10px;color:var(--text4);margin-top:4px">probabilistic &middot; float [0,1]</div>
      </div>
      <div style="display:flex;align-items:center;font-size:20px;color:var(--border2);padding:0 6px">&#8594;</div>
      <div style="flex:1;min-width:160px;background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r8);padding:14px">
        <div style="font-size:11px;font-weight:700;color:var(--good)">DETERMINISTIC POLICY</div>
        <div style="font-size:10.5px;color:var(--text3);margin-top:6px">V4_DEGRADATION_DEMO_POLICY_V1</div>
        <div style="font-size:10.5px;color:var(--text3)">&rarr; risk_level &middot; evidence_required</div>
        <div style="font-size:10px;color:var(--text4);margin-top:4px">fixed thresholds &middot; no actuation</div>
      </div>
      <div style="display:flex;align-items:center;font-size:20px;color:var(--border2);padding:0 6px">&#8594;</div>
      <div style="flex:1;min-width:160px;background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r8);padding:14px">
        <div style="font-size:11px;font-weight:700;color:var(--text2)">RESILIENCE STATE</div>
        <div style="font-size:10.5px;color:var(--text3);margin-top:6px">local_inference_allowed</div>
        <div style="font-size:10.5px;color:var(--text3)">local_buffering_required</div>
        <div style="font-size:10.5px;color:var(--text3)">synchronization_ready</div>
      </div>
    </div>
    <div style="margin-top:10px;font-size:11.5px;color:var(--text3)">AI components do not directly command vehicle actuation. All safety-relevant state transitions are deterministic.</div>
  </div>

  <!-- SYNC INFO -->
  <div class="card">
    <div class="card-hd">Synchronization &mdash; Software Manifest Only</div>
    <div class="g3">
      <div>
        <div class="mrow"><span class="mlabel">Sync type</span><span class="mval">Software manifest</span></div>
        <div class="mrow"><span class="mlabel">Network transmission</span><span class="mval" style="color:var(--danger)">NOT PERFORMED</span></div>
      </div>
      <div>
        <div class="mrow"><span class="mlabel">Cloud endpoint</span><span class="mval" style="color:var(--danger)">NOT CONTACTED</span></div>
        <div class="mrow"><span class="mlabel">Manifest contents</span><span class="mval">event IDs + digests</span></div>
      </div>
      <div>
        <div class="mrow"><span class="mlabel">Evidence integrity</span><span class="mval" style="color:var(--good)">SHA-256 hashed</span></div>
        <div class="mrow"><span class="mlabel">Buffer limit</span><span class="mval">100 records</span></div>
      </div>
    </div>
  </div>
</div>
""")
P3.append("""
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: EVIDENCE                                                  -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page" id="page-evidence">
  <div class="sec-hd">
    <div class="sec-eyebrow">Trust Infrastructure</div>
    <div class="sec-title">Evidence Ledger</div>
    <div class="sec-sub">SHA-256 hashed chain of custody &mdash; software simulation &mdash; no network transmission</div>
  </div>

  <!-- EVIDENCE CHAIN -->
  <div style="background:var(--purple-dim);border:1px solid rgba(167,139,250,.25);border-radius:var(--r12);padding:14px 18px;margin-bottom:16px">
    <div style="font-size:10px;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px">Evidence Chain</div>
    <div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px;font-size:12px;color:var(--text2)">
      <span style="background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r4);padding:4px 10px">Prediction</span>
      <span style="color:var(--text3)">&#8594;</span>
      <span style="background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r4);padding:4px 10px">Risk Assessment</span>
      <span style="color:var(--text3)">&#8594;</span>
      <span style="background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r4);padding:4px 10px">Resilience Response</span>
      <span style="color:var(--text3)">&#8594;</span>
      <span style="background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r4);padding:4px 10px">SHA-256 Record</span>
      <span style="color:var(--text3)">&#8594;</span>
      <span style="background:var(--surface2);border:1px solid var(--border2);border-radius:var(--r4);padding:4px 10px">Sync Manifest</span>
    </div>
  </div>

  <!-- TRUST LAYER -->
  <div class="g2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-hd">Trust &amp; Verification Status</div>
      <div class="trust-row">
        <div><div class="trust-name">Model Integrity</div><div class="trust-detail">temporal_predictor_v4.pt</div></div>
        <span class="badge badge-v">VERIFIED</span>
      </div>
      <div class="trust-row">
        <div><div class="trust-name">Data Artifact</div><div class="trust-detail">edgeresilience_temporal_dataset_v4.jsonl</div></div>
        <span class="badge badge-v">VERIFIED</span>
      </div>
      <div class="trust-row">
        <div><div class="trust-name">ONNX Equivalence</div><div class="trust-detail">max error 5.96e-08 &lt; threshold 1e-5</div></div>
        <span class="badge badge-v">VERIFIED</span>
      </div>
      <div class="trust-row">
        <div><div class="trust-name">Evidence Integrity</div><div class="trust-detail">SHA-256 hashed records</div></div>
        <span class="badge badge-v">VERIFIED</span>
      </div>
      <div class="trust-row">
        <div><div class="trust-name">Snapdragon Hardware</div><div class="trust-detail">Awaiting target-device validation</div></div>
        <span class="badge badge-p">NOT VERIFIED</span>
      </div>
      <div class="trust-row">
        <div><div class="trust-name">Physical Vehicle</div><div class="trust-detail">Software simulation environment</div></div>
        <span class="badge badge-d">NOT CONNECTED</span>
      </div>
    </div>

    <div class="card">
      <div class="card-hd">Evidence Integrity</div>
      <div class="mrow"><span class="mlabel">Hash algorithm</span><span class="mval">SHA-256</span></div>
      <div class="mrow"><span class="mlabel">Timestamp</span><span class="mval">UTC</span></div>
      <div class="mrow"><span class="mlabel">Format</span><span class="mval">Canonicalized JSON</span></div>
      <div class="mrow"><span class="mlabel">Buffer limit</span><span class="mval">100 records</span></div>
      <div class="mrow"><span class="mlabel">Network transmission</span><span class="mval" style="color:var(--danger)">NOT PERFORMED</span></div>
      <div class="mrow"><span class="mlabel">Physical forensics</span><span class="mval" style="color:var(--danger)">NOT CLAIMED</span></div>
      <div class="mrow"><span class="mlabel">Source file</span><span class="mval" style="font-size:10px">v4_demo_scenario.json</span></div>
    </div>
  </div>

  <!-- EVENT RECORDS -->
  <div class="card" style="margin-bottom:16px">
    <div class="card-hd">Event Records &mdash; Click to expand</div>
    <div id="evidence-rows"><div class="loading"><div class="spinner"></div>Loading&hellip;</div></div>
  </div>

  <!-- CHECKSUMS -->
  <div class="card">
    <div class="card-hd">Protected Artifact Checksums</div>
    <div class="hash-box">
      <span class="hash-label">V4 Model Checkpoint &mdash; temporal_predictor_v4.pt</span>
      <span class="hash-val">b551ad9f02b56668ef3f8f7873133748275307f1934ec7fd77da14e7325d26b9</span>
    </div>
    <div class="hash-box">
      <span class="hash-label">V4 Dataset &mdash; edgeresilience_temporal_dataset_v4.jsonl</span>
      <span class="hash-val">02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911</span>
    </div>
    <div class="hash-box">
      <span class="hash-label">Dynamic ONNX &mdash; temporal_predictor_v4_dynamic.onnx</span>
      <span class="hash-val">ACB43A20C9FA64577C56BDFE3AA3C2EA96B6691420C0A7994DC5FD9F230C0E5D</span>
    </div>
  </div>
</div>

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: DEPLOYMENT                                                -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page" id="page-deploy">
  <div class="sec-hd">
    <div class="sec-eyebrow">Edge Deployment</div>
    <div class="sec-title">Snapdragon-Targeted Deployment Journey</div>
    <div class="sec-sub">Engineering progression toward Snapdragon hardware validation &mdash; honest status at every stage</div>
  </div>

  <!-- HONESTY NOTICE -->
  <div style="background:var(--warn-dim);border:1px solid var(--warn-border);border-radius:var(--r12);padding:14px 18px;margin-bottom:20px">
    <div style="font-size:12px;font-weight:700;color:var(--warn);margin-bottom:5px">&#9888; CPU-to-CPU Benchmark Notice</div>
    <div style="font-size:12px;color:var(--text2);line-height:1.6">The ~5.99&times; speedup is a <strong>CPU-to-CPU reference benchmark</strong> on Intel Core i5-1235U. It is <strong>NOT</strong> a Snapdragon result, NOT an NPU result, and NOT a Qualcomm performance claim. Snapdragon hardware execution has <strong>NOT been verified</strong>.</div>
  </div>

  <div class="g2" style="margin-bottom:16px">

    <!-- SNAPDRAGON COMPONENT EVIDENCE -->
    <div class="card">
      <div class="card-hd">Snapdragon Deployment Evidence</div>
      <div style="font-size:11px;color:var(--text3);margin:-4px 0 14px">
        Qualcomm Snapdragon X Elite CRD &middot; Windows 11 &middot; QNN / HTP
      </div>

      <div class="trust-row">
        <div>
          <div class="trust-name">Encoder Block 1</div>
          <div style="font-size:10px;color:var(--text3)">Exact V4 graph &middot; 41 NPU layers</div>
        </div>
        <div style="text-align:right">
          <span class="badge badge-v">VERIFIED</span>
          <div style="font:600 11px var(--mono);margin-top:4px">0.045 ms</div>
        </div>
      </div>

      <div class="trust-row">
        <div>
          <div class="trust-name">Encoder Block 2</div>
          <div style="font-size:10px;color:var(--text3)">Exact V4 graph &middot; 40 NPU layers</div>
        </div>
        <div style="text-align:right">
          <span class="badge badge-v">VERIFIED</span>
          <div style="font:600 11px var(--mono);margin-top:4px">0.042 ms</div>
        </div>
      </div>

      <div class="trust-row">
        <div>
          <div class="trust-name">Temporal Pooling</div>
          <div style="font-size:10px;color:var(--text3)">Exact V4 graph &middot; 24 NPU layers</div>
        </div>
        <div style="text-align:right">
          <span class="badge badge-v">VERIFIED</span>
          <div style="font:600 11px var(--mono);margin-top:4px">0.038 ms</div>
        </div>
      </div>

      <div class="trust-row">
        <div>
          <div class="trust-name">Prediction Head</div>
          <div style="font-size:10px;color:var(--text3)">Exact V4 structure and weights</div>
        </div>
        <span class="badge badge-v">HTP VERIFIED</span>
      </div>

      <div style="margin-top:14px;padding:11px 13px;background:var(--warn-dim);border:1px solid var(--warn-border);border-radius:var(--r8)">
        <div style="font-size:11px;font-weight:700;color:var(--warn);margin-bottom:4px">
          Full V4 HTP execution
        </div>
        <div style="font-size:10.5px;color:var(--text2);line-height:1.5">
          Full graph compilation is verified. Full HTP execution remains
          <strong>NOT VERIFIED</strong> due to QNN graph finalization failure.
        </div>
      </div>

      <div style="margin-top:11px;font-size:10px;color:var(--text3);line-height:1.5">
        Component measurements are independent evidence and must not be summed
        into a full-model latency or memory claim.
      </div>
    </div>

    <!-- STATUS MATRIX + BENCHMARK -->
    <div>
      <div class="card" style="margin-bottom:14px">
        <div class="card-hd">Deployment Status Matrix</div>
        <div class="trust-row"><div class="trust-name">PyTorch Model (CPU reference)</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">ONNX Export (static)</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">ONNX Export (dynamic batch)</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">ONNX Numerical Equivalence</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">Snapdragon Deployment Package</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">QNN Compilation</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">QNN / HTP Component Execution</div><span class="badge badge-v">VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">Full V4 HTP Execution</div><span class="badge badge-p">NOT VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">Power Measurement</div><span class="badge badge-p">NOT VERIFIED</span></div>
        <div class="trust-row"><div class="trust-name">Thermal Measurement</div><span class="badge badge-p">NOT VERIFIED</span></div>
      </div>

      <div class="card">
        <div class="card-hd">CPU-to-CPU Reference Benchmark &mdash; NOT Snapdragon</div>
        <div style="font-size:10.5px;color:var(--warn);margin-bottom:10px;font-weight:600">&#9888; Intel Core i5-1235U &middot; CPU reference only</div>
        <div class="mrow"><span class="mlabel">PyTorch mean latency</span><span class="mval">1.656 ms</span></div>
        <div class="mrow"><span class="mlabel">ONNX mean latency</span><span class="mval">0.277 ms</span></div>
        <div class="mrow"><span class="mlabel">CPU-to-CPU speedup</span><span class="mval" style="color:var(--accent)">~5.99&times;</span></div>
        <div class="mrow"><span class="mlabel">Input shape</span><span class="mval">[1, 12, 17]</span></div>
        <div class="mrow"><span class="mlabel">Snapdragon result</span><span class="mval" style="color:var(--danger)">NOT MEASURED</span></div>
      </div>
    </div>
  </div>

  <!-- ROADMAP -->
  <div class="card">
    <div class="card-hd">Future Roadmap</div>
    <div class="roadmap-item">
      <div class="roadmap-num">1</div>
      <div style="flex:1"><div class="roadmap-title">Snapdragon Hardware Validation <span class="badge badge-fut" style="margin-left:8px">FUTURE</span></div><div class="roadmap-sub">Full-model HTP execution, power and thermal measurement on target Snapdragon hardware</div></div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-num">2</div>
      <div style="flex:1"><div class="roadmap-title">V2X Cooperative Cyber Resilience <span class="badge badge-fut" style="margin-left:8px">FUTURE</span></div><div class="roadmap-sub">Multi-vehicle simulation, cooperative threat detection</div></div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-num">3</div>
      <div style="flex:1"><div class="roadmap-title">Geographic Threat Clustering <span class="badge badge-fut" style="margin-left:8px">FUTURE</span></div><div class="roadmap-sub">Spatial anomaly correlation across vehicle fleet</div></div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-num">4</div>
      <div style="flex:1"><div class="roadmap-title">Mock City / Public-Safety Alert Interface <span class="badge badge-fut" style="margin-left:8px">FUTURE</span></div><div class="roadmap-sub">Simulation only &mdash; no real emergency dispatch</div></div>
    </div>
  </div>
</div>
""")
P3.append("""
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<!-- PAGE: SYSTEM EXPLORER                                           -->
<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
<div class="page" id="page-system">
  <div class="sec-hd">
    <div class="sec-eyebrow">Engineering Depth</div>
    <div class="sec-title">System Explorer</div>
    <div class="sec-sub">Technical deep-dive &mdash; model, data, policy, provenance, safety, reproducibility</div>
  </div>

  <div class="acc-hd open" onclick="toggleAcc(this)" aria-expanded="true">Model Card <span class="chev">&#8964;</span></div>
  <div class="acc-body open">
    <div class="g2">
      <div>
        <div class="mrow"><span class="mlabel">Name</span><span class="mval" style="font-size:10.5px">EdgeResilience_V4_TemporalPredictor</span></div>
        <div class="mrow"><span class="mlabel">Architecture</span><span class="mval">Temporal Transformer</span></div>
        <div class="mrow"><span class="mlabel">Parameters</span><span class="mval">71,170</span></div>
        <div class="mrow"><span class="mlabel">Input</span><span class="mval">17 features &times; 12 steps</span></div>
        <div class="mrow"><span class="mlabel">Output</span><span class="mval">future_degradation [0,1]</span></div>
        <div class="mrow"><span class="mlabel">Test MAE</span><span class="mval" style="color:var(--good)">0.0051</span></div>
        <div class="mrow"><span class="mlabel">Test RMSE</span><span class="mval" style="color:var(--good)">0.0066</span></div>
      </div>
      <div>
        <div class="mrow"><span class="mlabel">Checkpoint</span><span class="mval" style="font-size:10px">temporal_predictor_v4.pt</span></div>
        <div class="mrow"><span class="mlabel">Provenance</span><span class="mval" style="color:var(--accent)">NEW EdgeResilience</span></div>
        <div class="mrow"><span class="mlabel">Physical vehicle test</span><span class="mval" style="color:var(--danger)">NO</span></div>
        <div class="mrow"><span class="mlabel">Snapdragon HW verified</span><span class="mval" style="color:var(--warn)">NO</span></div>
        <div class="mrow"><span class="mlabel">External CAN</span><span class="mval" style="color:var(--danger)">NO</span></div>
        <div class="mrow"><span class="mlabel">Direct actuation</span><span class="mval" style="color:var(--danger)">NO</span></div>
      </div>
    </div>
  </div>

  <div class="acc-hd" onclick="toggleAcc(this)" aria-expanded="false">Data Card <span class="chev">&#8964;</span></div>
  <div class="acc-body">
    <div class="mrow"><span class="mlabel">Dataset</span><span class="mval" style="font-size:10px">edgeresilience_temporal_dataset_v4.jsonl</span></div>
    <div class="mrow"><span class="mlabel">Records</span><span class="mval">5,000</span></div>
    <div class="mrow"><span class="mlabel">Features per step</span><span class="mval">17</span></div>
    <div class="mrow"><span class="mlabel">Steps</span><span class="mval">12</span></div>
    <div class="mrow"><span class="mlabel">Generation</span><span class="mval">Synthetic EdgeResilience temporal scenarios</span></div>
    <div class="mrow"><span class="mlabel">Raw HCRL input</span><span class="mval" style="color:var(--danger)">NOT direct model input</span></div>
    <div class="mrow"><span class="mlabel">SHA-256</span><span class="mval" style="font-size:10px;color:var(--accent)">02a82f0f5ee78dc4e3be28b81b53b6eb4eb884600a4734f3eb3aaa279cb3a911</span></div>
    <div style="margin-top:14px">
      <div class="card-hd">17 Input Features &mdash; Signal Intelligence Contract</div>
      <div class="feat-grid" id="explore-features"></div>
    </div>
  </div>

  <div class="acc-hd" onclick="toggleAcc(this)" aria-expanded="false">Risk Policy <span class="chev">&#8964;</span></div>
  <div class="acc-body">
    <div class="mrow"><span class="mlabel">Policy name</span><span class="mval">V4_DEGRADATION_DEMO_POLICY_V1</span></div>
    <div class="mrow"><span class="mlabel">Type</span><span class="mval">Deterministic interpretation</span></div>
    <div class="mrow"><span class="mlabel">Learned thresholds</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Vehicle safety limits</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Snapdragon hardware limits</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Regulatory certification</span><span class="mval" style="color:var(--danger)">NO</span></div>
  </div>

  <div class="acc-hd" onclick="toggleAcc(this)" aria-expanded="false">Provenance Register <span class="chev">&#8964;</span></div>
  <div class="acc-body">
    <div class="prov-row prov-hd"><div>Artifact</div><div>Classification</div><div>Status</div></div>
    <div class="prov-row"><div class="prov-name">temporal_predictor_v4.pt</div><div class="prov-class">NEW EdgeResilience</div><div><span class="badge badge-v">VALIDATED</span></div></div>
    <div class="prov-row"><div class="prov-name">temporal_predictor_v4_dynamic.onnx</div><div class="prov-class">NEW EdgeResilience</div><div><span class="badge badge-v">VALIDATED</span></div></div>
    <div class="prov-row"><div class="prov-name">edgeresilience_temporal_dataset_v4.jsonl</div><div class="prov-class">NEW EdgeResilience</div><div><span class="badge badge-v">VALIDATED</span></div></div>
    <div class="prov-row"><div class="prov-name">v4_demo_scenario.json</div><div class="prov-class">NEW EdgeResilience</div><div><span class="badge badge-v">VALIDATED</span></div></div>
    <div class="prov-row"><div class="prov-name">src/vehicle/*_inherited.py</div><div class="prov-class">INHERITED / reference</div><div><span class="badge badge-i">NOT USED V4</span></div></div>
    <div class="prov-row"><div class="prov-name">inherited/Predictive-Cyber-Physical-Resilience/</div><div class="prov-class">INHERITED / reference</div><div><span class="badge badge-i">REFERENCE ONLY</span></div></div>
  </div>

  <div class="acc-hd" onclick="toggleAcc(this)" aria-expanded="false">Validation Evidence <span class="chev">&#8964;</span></div>
  <div class="acc-body">
    <div class="mrow"><span class="mlabel">V4 training</span><span class="mval" style="color:var(--good)">MAE 0.0051, RMSE 0.0066</span></div>
    <div class="mrow"><span class="mlabel">Temporal ablation</span><span class="mval" style="color:var(--good)">Full sequence strongest neural</span></div>
    <div class="mrow"><span class="mlabel">ONNX static equivalence</span><span class="mval" style="color:var(--good)">PASS</span></div>
    <div class="mrow"><span class="mlabel">ONNX dynamic equivalence</span><span class="mval" style="color:var(--good)">PASS (max err 5.96e-08)</span></div>
    <div class="mrow"><span class="mlabel">CPU benchmark</span><span class="mval" style="color:var(--good)">36,152 samples/sec</span></div>
    <div class="mrow"><span class="mlabel">ONNX CPU speedup</span><span class="mval" style="color:var(--accent)">~5.99&times; CPU-to-CPU</span></div>
    <div class="mrow"><span class="mlabel">Three-cycle demo</span><span class="mval" style="color:var(--good)">PASS</span></div>
    <div class="mrow"><span class="mlabel">Snapdragon hardware</span><span class="mval" style="color:var(--warn)">NOT VERIFIED</span></div>
  </div>

  <div class="acc-hd" onclick="toggleAcc(this)" aria-expanded="false">Safety Boundary <span class="chev">&#8964;</span></div>
  <div class="acc-body">
    <div style="font-size:13px;font-weight:700;color:var(--warn);margin-bottom:10px">SOFTWARE SIMULATION / VIRTUAL VEHICLE / VIRTUAL CAN LAB</div>
    <div class="mrow"><span class="mlabel">Physical vehicle testing</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Production vehicle connection</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">External CAN transmission</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Direct vehicle actuation</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Real emergency dispatch</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Fabricated telemetry</span><span class="mval" style="color:var(--danger)">NO</span></div>
    <div class="mrow"><span class="mlabel">Fabricated NPU metrics</span><span class="mval" style="color:var(--danger)">NO</span></div>
  </div>

  <div class="acc-hd" onclick="toggleAcc(this)" aria-expanded="false">Reproducibility <span class="chev">&#8964;</span></div>
  <div class="acc-body">
    <div style="font-size:12px;color:var(--text2);line-height:1.8;margin-bottom:10px">Requirements: Python 3.9+, PyTorch, ONNX Runtime, NumPy, scikit-learn</div>
    <div class="hash-box"><span class="hash-label">Install</span><span style="color:var(--text2)">pip install torch onnxruntime numpy scikit-learn joblib</span></div>
    <div class="hash-box"><span class="hash-label">Run Demo</span><span style="color:var(--text2)">python demo/run_demo.py</span></div>
    <div class="hash-box"><span class="hash-label">Run Dashboard</span><span style="color:var(--text2)">python src/dashboard/server.py</span></div>
  </div>
</div>

</div><!-- /shell -->
""")
P3.append("""
<script>
// â”€â”€ PAGE NAVIGATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const PAGE_TITLES = {
  cmd:'Command Center', demo:'Live Demo', ai:'AI Intelligence',
  resilience:'Resilience', evidence:'Evidence Ledger',
  deploy:'Edge Deployment', system:'System Explorer'
};
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  const pg = document.getElementById('page-' + id);
  const tb = document.getElementById('nav-' + id);
  if (pg) pg.classList.add('active');
  if (tb) tb.classList.add('active');
}

// â”€â”€ PRESENTATION MODE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
let presMode = false;
function togglePresMode() {
  presMode = !presMode;
  const btn = document.getElementById('pres-btn');
  if (presMode) {
    document.querySelectorAll('.acc-body:not(.open)').forEach(b => {});
    document.querySelectorAll('#page-system,#page-deploy .card:last-child').forEach(el => {
      if (el) el.style.display = presMode ? 'none' : '';
    });
    btn.classList.add('on');
    btn.textContent = '&#9632; Exit Present';
  } else {
    document.querySelectorAll('#page-system,#page-deploy .card:last-child').forEach(el => {
      if (el) el.style.display = '';
    });
    btn.classList.remove('on');
    btn.textContent = '&#9654; Present';
  }
}

// â”€â”€ ACCORDION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function toggleAcc(hd) {
  const isOpen = hd.classList.contains('open');
  hd.classList.toggle('open');
  hd.setAttribute('aria-expanded', !isOpen);
  const body = hd.nextElementSibling;
  if (body) body.classList.toggle('open');
}

// â”€â”€ COLOR HELPERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function riskColor(r) {
  return {NORMAL:'var(--good)',LOW:'var(--good)',MEDIUM:'var(--medium)',HIGH:'var(--warn)',CRITICAL:'var(--danger)'}[r]||'var(--text)';
}
function connColor(c) {
  return {CONNECTED:'var(--good)',DEGRADED:'var(--warn)',DISCONNECTED:'var(--danger)'}[c]||'var(--text)';
}

// â”€â”€ DEG BAR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function degBar(val, risk) {
  const pct = Math.min(val * 1000, 100).toFixed(1);
  const col = riskColor(risk);
  return `<div class="deg-wrap">
    <div class="deg-labels"><span>0</span><strong>${val.toFixed(4)}</strong><span>0.10</span></div>
    <div class="deg-bg"><div class="deg-fill" style="width:${pct}%;background:${col}"></div></div>
  </div>`;
}

// â”€â”€ CYCLE CARD â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function cycleCard(c, active) {
  const pred = c.prediction.predicted_future_degradation;
  const risk = c.risk.predictive_risk_level;
  const conn = c.connectivity_state;
  return `<div class="cycle-card${active?' cc-active':''}">
    <div class="cc-hd">
      <span class="cc-id">${c.cycle_id}</span>
      <span class="cc-label">${c.label}</span>
    </div>
    ${degBar(pred, risk)}
    <div class="cc-tags">
      <div class="ctag"><span class="ctag-l">Risk</span><span class="ctag-v" style="color:${riskColor(risk)}">${risk}</span></div>
      <div class="ctag"><span class="ctag-l">Connectivity</span><span class="ctag-v" style="color:${connColor(conn)}">${conn}</span></div>
      <div class="ctag"><span class="ctag-l">Local Inference</span><span class="ctag-v ctag-yes">ACTIVE</span></div>
      <div class="ctag"><span class="ctag-l">Buffering</span><span class="ctag-v ${c.local_buffering_required?'ctag-yes':'ctag-no'}">${c.local_buffering_required?'ACTIVE':'â€”'}</span></div>
      <div class="ctag"><span class="ctag-l">Recovery</span><span class="ctag-v ${c.recovery_detected?'ctag-yes':'ctag-no'}">${c.recovery_detected?'YES':'â€”'}</span></div>
      <div class="ctag"><span class="ctag-l">Sync Ready</span><span class="ctag-v ${c.synchronization_ready?'ctag-yes':'ctag-no'}">${c.synchronization_ready?'YES':'â€”'}</span></div>
      <div class="ctag"><span class="ctag-l">Evidence</span><span class="ctag-v">${c.evidence_count}</span></div>
    </div>
  </div>`;
}

// â”€â”€ LOAD EVIDENCE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
let EVIDENCE = null;
async function loadEvidence() {
  try {
    const r = await fetch('/api/evidence');
    EVIDENCE = await r.json();
    renderAll();
  } catch(e) {
    const hb = document.getElementById('cmd-hero-badges');
    if (hb) hb.innerHTML = '<span style="color:var(--danger);font-size:12px">Evidence load failed: ' + e.message + '</span>';
  }
}

function renderAll() {
  if (!EVIDENCE || !EVIDENCE.cycles) return;
  const cycles = EVIDENCE.cycles;
  const last = cycles[cycles.length - 1];
  renderCommandCenter(cycles, last);
  renderTimeline(cycles);
  renderTemporalSVG();
  renderAblation();
  renderResConnCycles(cycles);
  renderEvidenceRows(cycles);
  renderDemoAllCycles(cycles);
}

// â”€â”€ COMMAND CENTER â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function renderCommandCenter(cycles, last) {
  const pred = last.prediction.predicted_future_degradation;
  const risk = last.risk.predictive_risk_level;
  const conn = last.connectivity_state;
  const evCount = last.evidence_count;
  const rc = riskColor(risk);
  const cc = connColor(conn);

  const set = (id, val, col) => { const e = document.getElementById(id); if(e){e.textContent=val; if(col) e.style.color=col;} };
  set('sc-deg-val', pred.toFixed(4), rc);
  set('sc-risk-val', 'Predictive Risk: ' + risk, rc);
  set('sc-conn-val', conn, cc);
  set('sc-evcount', String(evCount));
  set('sc-sync', last.synchronization_ready ? 'SYNC READY' : 'No sync pending', last.synchronization_ready ? 'var(--good)' : null);
  set('fs-predict', pred.toFixed(4), rc);
  set('fs-risk', risk, rc);
  set('fs-buf', evCount + ' records');
  set('fs-sync', last.synchronization_ready ? 'READY' : 'â€”', last.synchronization_ready ? 'var(--good)' : 'var(--text3)');

  // flow step states
  const assessStep = document.getElementById('fs-assess-step');
  if (assessStep) {
    assessStep.className = 'flow-step ' + ({NORMAL:'fs-good',LOW:'fs-good',MEDIUM:'fs-warn',HIGH:'fs-warn',CRITICAL:'fs-danger'}[risk]||'');
  }
  const preserveStep = document.getElementById('fs-preserve-step');
  if (preserveStep) preserveStep.className = 'flow-step ' + (last.local_buffering_required ? 'fs-warn' : '');
  const recoverStep = document.getElementById('fs-recover-step');
  if (recoverStep) recoverStep.className = 'flow-step ' + (last.synchronization_ready ? 'fs-good' : '');

  const hb = document.getElementById('cmd-hero-badges');
  if (hb) hb.innerHTML = '<span class="badge badge-v">CPU VERIFIED</span> <span class="badge badge-v">ONNX VERIFIED</span> <span class="badge badge-p">SNAPDRAGON NOT VERIFIED</span> <span class="badge badge-i">V4 &middot; 71,170 params</span> <span class="badge badge-i">MAE 0.0051</span> <span class="badge badge-i">SOFTWARE SIMULATION</span>';
}

function renderTimeline(cycles) {
  const el = document.getElementById('cmd-timeline');
  if (el) el.innerHTML = cycles.map((c, i) => cycleCard(c, i === cycles.length - 1)).join('');
}

// â”€â”€ TEMPORAL SVG VISUALIZATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function renderTemporalSVG() {
  const svg = document.getElementById('ai-temporal-svg');
  if (!svg) return;
  const heights = [28,35,40,33,48,52,45,58,50,55,62,68];
  const W = 400, H = 80, barW = 22, gap = 4;
  const obsCount = 12;
  const totalObs = obsCount * (barW + gap);
  const predW = 36;
  let html = '';
  // gradient defs
  html += '<defs><linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/><stop offset="100%" stop-color="#0ea5e9" stop-opacity="0.4"/></linearGradient><linearGradient id="predGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#fbbf24" stop-opacity="0.9"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.4"/></linearGradient></defs>';
  // observed bars
  for (let i = 0; i < obsCount; i++) {
    const h = (heights[i] / 100) * (H - 10);
    const x = i * (barW + gap);
    const y = H - h;
    const opacity = 0.35 + (i / obsCount) * 0.65;
    html += `<rect x="${x}" y="${y}" width="${barW}" height="${h}" rx="2" fill="url(#barGrad)" opacity="${opacity.toFixed(2)}"/>`;
  }
  // prediction boundary line
  const boundX = totalObs + 2;
  html += `<line x1="${boundX}" y1="0" x2="${boundX}" y2="${H}" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.7"/>`;
  // predicted bar
  const predH = (0.75) * (H - 10);
  const predY = H - predH;
  html += `<rect x="${boundX + 6}" y="${predY}" width="${predW}" height="${predH}" rx="2" fill="url(#predGrad)" opacity="0.8"/>`;
  // label
  html += `<text x="${boundX + 6 + predW/2}" y="${predY - 4}" text-anchor="middle" font-size="8" fill="#fbbf24" font-family="monospace">PRED</text>`;
  svg.innerHTML = html;
}

// â”€â”€ ABLATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function renderAblation() {
  const el = document.getElementById('ai-ablation');
  if (!el) return;
  const rows = [
    {label:'Full 12-step sequence', mae:0.0052, best:true},
    {label:'Final + delta + std (compact)', mae:0.0053, best:false},
    {label:'Final timestep only', mae:0.0067, best:false}
  ];
  const maxMae = 0.008;
  el.innerHTML = rows.map(r => `
    <div class="abl-row">
      <span class="abl-label ${r.best?'abl-best':''}">${r.label}${r.best?' &#9733; best':''}</span>
      <div class="abl-bar-wrap"><div class="abl-bar" style="width:${(r.mae/maxMae*100).toFixed(1)}%;background:${r.best?'var(--good)':'var(--accent)'}"></div></div>
      <span class="abl-val ${r.best?'abl-best':''}">MAE ${r.mae}</span>
    </div>`).join('');
}

// â”€â”€ RESILIENCE CONN CYCLES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function renderResConnCycles(cycles) {
  const el = document.getElementById('res-conn-cycles');
  if (!el) return;
  el.innerHTML = cycles.map(c => {
    const conn = c.connectivity_state;
    return `<div style="padding:10px 0;border-bottom:1px solid var(--border)">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">
        <span style="font-size:11px;font-weight:700;font-family:var(--mono);color:var(--accent)">${c.cycle_id}</span>
        <span style="font-size:12px;font-weight:700;color:${connColor(conn)}">${conn}</span>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:8px">
        <span style="font-size:10.5px;color:var(--good)">&#9679; Local inference: ACTIVE</span>
        <span style="font-size:10.5px;color:${c.local_buffering_required?'var(--warn)':'var(--text3)'}">&#9679; Buffering: ${c.local_buffering_required?'ACTIVE':'â€”'}</span>
        <span style="font-size:10.5px;color:${c.recovery_detected?'var(--good)':'var(--text3)'}">&#9679; Recovery: ${c.recovery_detected?'DETECTED':'â€”'}</span>
        <span style="font-size:10.5px;color:${c.synchronization_ready?'var(--good)':'var(--text3)'}">&#9679; Sync: ${c.synchronization_ready?'READY':'â€”'}</span>
      </div>
    </div>`;
  }).join('');
}

// â”€â”€ EVIDENCE ROWS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
function renderEvidenceRows(cycles) {
  const el = document.getElementById('evidence-rows');
  if (!el) return;
  el.innerHTML = cycles.map((c, idx) => {
    const pred = c.prediction.predicted_future_degradation;
    const risk = c.risk.predictive_risk_level;
    const flags = [
      c.local_inference_allowed ? 'LOCAL_INFERENCE' : null,
      c.local_buffering_required ? 'BUFFERING' : null,
      c.recovery_detected ? 'RECOVERY' : null,
      c.synchronization_ready ? 'SYNC_READY' : null
    ].filter(Boolean).join(' | ') || 'â€”';
    const bodyId = 'ev-body-' + idx;
    return `<div style="border-bottom:1px solid var(--border)">
      <div style="display:flex;align-items:center;gap:12px;padding:11px 14px;cursor:pointer;transition:background var(--t150)" onclick="toggleEvRow('${bodyId}',this)" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background=''">
        <span style="font-family:var(--mono);font-size:11px;color:var(--accent);width:90px;flex-shrink:0">${c.cycle_id}</span>
        <span style="font-weight:700;color:${connColor(c.connectivity_state)};font-size:11px;width:110px;flex-shrink:0">${c.connectivity_state}</span>
        <span style="font-weight:700;color:${riskColor(risk)};font-size:11px;width:80px;flex-shrink:0">${risk}</span>
        <span style="font-family:var(--mono);font-size:11px;width:70px;flex-shrink:0">${pred.toFixed(4)}</span>
        <span style="font-size:10.5px;color:var(--text3);flex:1">${flags}</span>
        <span style="font-size:10px;color:var(--text3)">&#8964;</span>
      </div>
      <div id="${bodyId}" style="display:none;padding:12px 14px 14px;background:var(--surface2);border-top:1px solid var(--border)">
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;font-size:11px">
          <div><span style="color:var(--text3)">Model: </span><span style="color:var(--accent)">${c.prediction.model_name}</span></div>
          <div><span style="color:var(--text3)">Policy: </span><span style="color:var(--text)">${c.risk.policy_name}</span></div>
          <div><span style="color:var(--text3)">Evidence required: </span><span style="color:${c.risk.evidence_required?'var(--warn)':'var(--good)'}">${c.risk.evidence_required?'YES':'NO'}</span></div>
          <div><span style="color:var(--text3)">Evidence count: </span><span style="color:var(--text)">${c.evidence_count}</span></div>
          <div><span style="color:var(--text3)">Sync allowed: </span><span style="color:${c.synchronization_allowed?'var(--good)':'var(--text3)'}">${c.synchronization_allowed?'YES':'NO'}</span></div>
          <div><span style="color:var(--text3)">Reason codes: </span><span style="color:var(--text2);font-family:var(--mono);font-size:10px">${c.reason_codes.join(', ')||'â€”'}</span></div>
        </div>
      </div>
    </div>`;
  }).join('');
}

function toggleEvRow(bodyId, hdr) {
  const body = document.getElementById(bodyId);
  if (!body) return;
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  const chev = hdr.querySelector('span:last-child');
  if (chev) chev.style.transform = open ? '' : 'rotate(180deg)';
}

// â”€â”€ DEMO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
let demoStep = 0;
let autoTimer = null;

function renderDemoAllCycles(cycles) {
  const el = document.getElementById('demo-all-cycles');
  if (el) el.innerHTML = cycles.map((c, i) => cycleCard(c, i === demoStep - 1)).join('');
}

const SM_NODES = ['observe','predict','assess','respond','preserve','recover'];

function setSmState(activeIdx) {
  SM_NODES.forEach((n, i) => {
    const dot = document.getElementById('sm-dot-' + n);
    if (!dot) return;
    if (i < activeIdx) dot.className = 'sm-dot sm-done';
    else if (i === activeIdx) dot.className = 'sm-dot sm-active';
    else dot.className = 'sm-dot';
  });
}

function setSmActivity(node, text) {
  const el = document.getElementById('sm-act-' + node);
  if (el) el.textContent = text;
}

function clearSmActivities() {
  SM_NODES.forEach(n => setSmActivity(n, ''));
}

function stepDemo() {
  if (!EVIDENCE || !EVIDENCE.cycles) return;
  const cycles = EVIDENCE.cycles;
  if (demoStep >= cycles.length) {
    demoStep = 0;
    document.getElementById('demo-conclusion').style.display = 'none';
  }
  const prev = demoStep > 0 ? cycles[demoStep - 1] : null;
  const c = cycles[demoStep];
  demoStep++;

  const pred = c.prediction.predicted_future_degradation;
  const risk = c.risk.predictive_risk_level;
  const conn = c.connectivity_state;
  const rc = riskColor(risk);
  const cc = connColor(conn);

  document.getElementById('demo-step-label').textContent = 'Cycle ' + demoStep + ' of ' + cycles.length + ' â€” ' + c.label;

  // State machine animation
  clearSmActivities();
  setSmState(5); // all done after full cycle
  setSmActivity('observe', '17 features Ã— 12 steps ingested');
  setSmActivity('predict', 'future_degradation = ' + pred.toFixed(4));
  setSmActivity('assess', risk + (c.risk.evidence_required ? ' â€” evidence required' : ' â€” no evidence required'));
  setSmActivity('respond', conn + ' â€” local inference: ACTIVE');
  setSmActivity('preserve', c.local_buffering_required ? 'ACTIVE â€” ' + c.evidence_count + ' records buffered' : 'inactive â€” no buffering required');
  setSmActivity('recover', c.synchronization_ready ? 'RECOVERY DETECTED â€” sync manifest prepared' : (c.recovery_detected ? 'recovery detected' : 'â€”'));

  // Spotlight
  document.getElementById('demo-spotlight').innerHTML = `
    <div class="card-hd">Active Cycle â€” ${c.cycle_id}</div>
    <div style="font-size:14px;font-weight:700;color:var(--text);margin-bottom:10px">${c.label}</div>
    ${degBar(pred, risk)}
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
      <span class="badge" style="color:${rc};border-color:${rc};background:var(--surface2)">${risk}</span>
      <span class="badge" style="color:${cc};border-color:${cc};background:var(--surface2)">${conn}</span>
      ${c.local_buffering_required ? '<span class="badge badge-p">BUFFERING ACTIVE</span>' : ''}
      ${c.recovery_detected ? '<span class="badge badge-v">RECOVERY DETECTED</span>' : ''}
      ${c.synchronization_ready ? '<span class="badge badge-v">SYNC READY</span>' : ''}
    </div>
    <div style="margin-top:10px;font-size:11px;color:var(--text3)">${c.reason_codes.join(' Â· ')}</div>`;

  // Transition panel
  const cmpEl = document.getElementById('demo-transition');
  if (cmpEl) {
    cmpEl.style.display = prev ? 'block' : 'none';
    if (prev) {
      const pp = prev.prediction.predicted_future_degradation;
      const pr = prev.risk.predictive_risk_level;
      const pc = prev.connectivity_state;
      document.getElementById('demo-prev-state').innerHTML =
        `<div style="font-size:9px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Previous â€” ${prev.cycle_id}</div>
         <div style="font-size:18px;font-weight:900;color:${riskColor(pr)}">${pr}</div>
         <div style="font-size:11px;color:var(--text3);margin-top:2px">${pp.toFixed(4)}</div>
         <div style="font-size:13px;font-weight:700;color:${connColor(pc)};margin-top:6px">${pc}</div>`;
      document.getElementById('demo-curr-state').innerHTML =
        `<div style="font-size:9px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Current â€” ${c.cycle_id}</div>
         <div style="font-size:18px;font-weight:900;color:${rc}">${risk}</div>
         <div style="font-size:11px;color:var(--text3);margin-top:2px">${pred.toFixed(4)}</div>
         <div style="font-size:13px;font-weight:700;color:${cc};margin-top:6px">${conn}</div>
         ${c.recovery_detected ? '<div style="font-size:10.5px;color:var(--good);margin-top:4px">&#9679; Recovery detected</div>' : ''}
         ${c.synchronization_ready ? '<div style="font-size:10.5px;color:var(--good);margin-top:2px">&#9679; Sync ready</div>' : ''}`;
    }
  }

  renderDemoAllCycles(cycles);

  // Show conclusion after last cycle
  if (demoStep === cycles.length) {
    setTimeout(() => {
      const conc = document.getElementById('demo-conclusion');
      if (conc) conc.style.display = 'block';
    }, 400);
  }
}

function autoPlay() {
  if (autoTimer) {
    clearInterval(autoTimer);
    autoTimer = null;
    document.getElementById('btn-auto').textContent = '\\u25b6\\u25b6 Auto Play';
    return;
  }
  document.getElementById('btn-auto').textContent = '&#9646;&#9646; Stop';
  autoTimer = setInterval(() => {
    if (!EVIDENCE) return;
    if (demoStep >= EVIDENCE.cycles.length) {
      clearInterval(autoTimer);
      autoTimer = null;
      document.getElementById('btn-auto').textContent = '\\u25b6\\u25b6 Auto Play';
      return;
    }
    stepDemo();
  }, 2200);
}

function resetDemo() {
  if (autoTimer) { clearInterval(autoTimer); autoTimer = null; }
  document.getElementById('btn-auto').textContent = '&#9654;&#9654; Auto Play';
  demoStep = 0;
  document.getElementById('demo-step-label').textContent = 'Press Next Cycle to begin';
  document.getElementById('demo-spotlight').innerHTML = '<div class="card-hd">Active Cycle</div><div style="color:var(--text3);font-size:12.5px">Press <strong style="color:var(--accent)">Next Cycle</strong> to begin the demonstration.</div>';
  const cmp = document.getElementById('demo-transition');
  if (cmp) cmp.style.display = 'none';
  const conc = document.getElementById('demo-conclusion');
  if (conc) conc.style.display = 'none';
  SM_NODES.forEach(n => {
    const dot = document.getElementById('sm-dot-' + n);
    if (dot) dot.className = 'sm-dot';
    setSmActivity(n, '');
  });
  if (EVIDENCE) renderDemoAllCycles(EVIDENCE.cycles);
}

// â”€â”€ FEATURES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const FEATURES = [
  'cyber_message_rate','cyber_unique_can_id_count','cyber_can_id_entropy',
  'cyber_mean_interarrival_ms','cyber_std_interarrival_ms','cyber_min_interarrival_ms',
  'cyber_max_interarrival_ms','cyber_interarrival_cv','cyber_payload_change_rate',
  'cyber_mean_hamming_distance','cyber_dlc_change_rate','cyber_dominant_can_id_fraction',
  'cyber_burst_score','cyber_timing_anomaly_score','cyber_payload_anomaly_score',
  'cyber_id_anomaly_score','cyber_attack_score'
];
const fg = document.getElementById('explore-features');
if (fg) fg.innerHTML = FEATURES.map((f,i) => `<div class="feat-item"><span class="feat-num">${i+1}</span>${f}</div>`).join('');

// â”€â”€ INIT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
loadEvidence();
</script>
</body>
</html>
""")

# Write part 3
(DASH / "_part3_pages.html").write_text("".join(P3), encoding="utf-8")
print("part3 written:", len("".join(P3)), "chars")
print("ALL PARTS WRITTEN SUCCESSFULLY")


