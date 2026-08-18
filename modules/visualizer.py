"""
CORPO-RECON :: Premium Topology Visualizer & Executive Dashboard
Generates a Palantir/Stripe-styled standalone HTML dashboard.
"""

from __future__ import annotations
import json
import os
from typing import Dict, Any

def generate_dashboard(recon_data: dict, output_dir: str) -> str:
    """
    Generate an ultra-premium dark-mode HTML dashboard integrating 
    financial intelligence and interactive network topology.
    """
    target = recon_data.get("scan_metadata", {}).get("target", "Target")
    timestamp = recon_data.get("scan_metadata", {}).get("timestamp", "")
    
    # Extract Financials
    fin = recon_data.get("financial_data", {})
    ticker = fin.get("ticker") or "N/A"
    stock_price = fin.get("stock_price")
    stock_price_display = f"${stock_price}" if stock_price is not None else "N/A"
    market_cap = fin.get("market_cap") or "N/A"
    risk_score = fin.get("risk_score", 0)
    
    # Extract metrics
    subdomains = recon_data.get("subdomains", [])
    live_hosts = recon_data.get("live_hosts", [])
    open_ports = recon_data.get("open_ports", {}).get("ports", [])
    cve_findings = recon_data.get("cve_findings", [])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Corpo-Recon Executive Dashboard :: {target}</title>
    <script src="https://unpkg.com/force-graph"></script>
    <style>
        :root {{
            --bg-base: #050505;
            --bg-surface: #111111;
            --text-primary: #ffffff;
            --text-secondary: #888888;
            --accent: #2b2b2b;
            --danger: #ff3333;
            --warning: #ffaa00;
            --success: #00ff66;
            --font-mono: 'SF Mono', 'Fira Code', 'Roboto Mono', monospace;
            --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }}
        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: var(--font-sans);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        #sidebar {{
            width: 380px;
            background-color: var(--bg-surface);
            border-right: 1px solid var(--accent);
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            overflow-y: auto;
            z-index: 10;
            box-shadow: 10px 0 30px rgba(0,0,0,0.5);
        }}
        #graph-container {{
            flex: 1;
            position: relative;
        }}
        .brand {{
            font-family: var(--font-mono);
            font-size: 0.8rem;
            letter-spacing: 4px;
            color: var(--text-secondary);
            text-transform: uppercase;
        }}
        h1 {{
            margin: 0.5rem 0 0 0;
            font-size: 2rem;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}
        .metric-card {{
            background: #1a1a1a;
            border: 1px solid var(--accent);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        .metric-card.alert {{
            border-color: rgba(255, 51, 51, 0.3);
            background: linear-gradient(145deg, #1a1a1a 0%, #2a0a0a 100%);
        }}
        .metric-title {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            font-family: var(--font-mono);
        }}
        .metric-value {{
            font-size: 2rem;
            font-weight: 300;
        }}
        .metric-sub {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }}
        .financial-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}
        .fin-item {{
            display: flex;
            flex-direction: column;
        }}
        .fin-label {{
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
        }}
        .fin-value {{
            font-size: 1.1rem;
            font-family: var(--font-mono);
            margin-top: 0.2rem;
        }}
        .status-badge {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-family: var(--font-mono);
            background: rgba(255, 51, 51, 0.1);
            color: var(--danger);
            border: 1px solid rgba(255, 51, 51, 0.2);
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <div id="sidebar">
        <div>
            <div class="brand">CORPO-RECON</div>
            <h1>{target}</h1>
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
                SCAN INITIATED: {timestamp}
            </div>
        </div>

        <div class="metric-card alert">
            <div class="metric-title">Composite Risk Score</div>
            <div class="metric-value">{risk_score}/100</div>
            <div class="metric-sub">Calculated via AI heuristics & SEC SEC filings</div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Financial Intelligence</div>
            <div class="financial-grid">
                <div class="fin-item">
                    <span class="fin-label">Ticker</span>
                    <span class="fin-value">{ticker}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Market Price</span>
                    <span class="fin-value">{stock_price_display}</span>
                </div>
                <div class="fin-item" style="grid-column: span 2;">
                    <span class="fin-label">Market Capitalization</span>
                    <span class="fin-value">{market_cap}</span>
                </div>
            </div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Attack Surface Footprint</div>
            <div class="financial-grid">
                <div class="fin-item">
                    <span class="fin-label">Subdomains</span>
                    <span class="fin-value" style="color: #fff;">{len(subdomains)}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Live Hosts</span>
                    <span class="fin-value" style="color: #fff;">{len(live_hosts)}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Open Ports</span>
                    <span class="fin-value" style="color: var(--warning);">{len(open_ports)}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Critical CVEs</span>
                    <span class="fin-value" style="color: var(--danger);">{len(cve_findings)}</span>
                </div>
            </div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Deep Recon Intel</div>
            <div class="financial-grid">
                <div class="fin-item">
                    <span class="fin-label">Threat Intel Flag</span>
                    <span class="fin-value" style="color: var(--danger);">{recon_data.get("threat_data", dict()).get("target_flagged", False)}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Sandbox Environment</span>
                    <span class="fin-value" style="color: #fff;">{recon_data.get("sandbox_data", dict()).get("environment", "Unknown")}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Email Infrastructure Security</span>
                    <span class="fin-value" style="color: var(--warning);">{recon_data.get("email_data", dict()).get("secure", False)}</span>
                </div>
                <div class="fin-item">
                    <span class="fin-label">Identified WAFs</span>
                    <span class="fin-value" style="color: #fff;">{len(recon_data.get("fingerprints", []))} Detected</span>
                </div>
            </div>
        </div>
        <div class="metric-card" style="margin-top: 1rem; border-color: rgba(255, 255, 255, 0.1);">
            <div class="metric-title">Target Intelligence (Screenshot)</div>
            <div style="width: 100%; height: 180px; overflow: hidden; border-radius: 6px; border: 1px solid var(--accent); margin-bottom: 1rem; background: #000;">
                <img src="https://image.thum.io/get/width/600/crop/800/https://{target}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IiMzMzMiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZmlsbD0iI2ZmZiIgZm9udC1mYW1pbHk9InNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTQiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5TY3JlZW5zaG90IFVuYXZhaWxhYmxlPC90ZXh0Pjwvc3ZnPg=='" alt="Target Screenshot" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.8) contrast(1.2);">
            </div>
        </div>

        <div class="metric-card" style="flex: 1; display: flex; flex-direction: column; overflow: hidden;">
            <div class="metric-title">AI Executive Summary</div>
            <div style="flex: 1; overflow-y: auto; font-family: var(--font-mono); font-size: 0.75rem; color: #a0a0a0; white-space: pre-wrap; line-height: 1.4; padding-right: 10px;">{recon_data.get('ai_report', 'AI Report not available. Run with --ai-report flag.')}</div>
        </div>
    </div>
    <div id="graph-container"></div>

    <script>
        // Transform Python recon data into Graph JSON format
        const targetDomain = "{target}";
        const rawSubdomains = {json.dumps(subdomains)};
        
        const nodes = [{{ id: targetDomain, group: 1, val: 20 }}];
        const links = [];
        
        // Add subdomain nodes
        rawSubdomains.forEach(sub => {{
            if(sub && !sub.includes("ERROR")) {{
                nodes.push({{ id: sub, group: 2, val: 5 }});
                links.push({{ source: targetDomain, target: sub }});
            }}
        }});
        
        const gData = {{ nodes, links }};

        const Graph = ForceGraph()(document.getElementById('graph-container'))
            .graphData(gData)
            .nodeId('id')
            .nodeVal('val')
            .nodeLabel('id')
            .nodeAutoColorBy('group')
            .linkColor(() => 'rgba(255,255,255,0.1)')
            .backgroundColor('#050505')
            .nodeCanvasObject((node, ctx, globalScale) => {{
                const label = node.id;
                const fontSize = 12/globalScale;
                ctx.font = `${{fontSize}}px Sans-Serif`;
                const textWidth = ctx.measureText(label).width;
                const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

                ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
                ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = node.color;
                ctx.fillText(label, node.x, node.y);

                node.__bckgDimensions = bckgDimensions;
            }})
            .nodePointerAreaPaint((node, color, ctx) => {{
                ctx.fillStyle = color;
                const bckgDimensions = node.__bckgDimensions;
                bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
            }});
            
        // Initial animation
        setTimeout(() => {{
            Graph.zoomToFit(400, 50);
        }}, 500);
    </script>
</body>
</html>
"""
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"dashboard_{target}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return out_path
