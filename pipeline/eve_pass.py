"""Stage 5 (optional) — eve pass over a heat map. Mirrors spectral-terrain scripts/geo_rag_ingest.py:
K-NN graph over the normalized structural fingerprints -> TriadGATGraphRAG.embed_graph -> GAT-space heat
(manhattan) and shatter (distance from centroid) per shard, plus the corpus GSI from rag_strike + diffusion_lock.
The GAT is untrained (random init, as in geo_rag_ingest): fingerprint heat stays the primary signal, GAT adds
relational context. Seeded so reruns match.

eve is NOT in this repo (its source gist is private). It is pinned at ~/.local/share/eve/eve_v1.py
(SOURCE.txt there says which gist revision) and runs under ~/.local/share/eve-venv:
  ~/.local/share/eve-venv/bin/python pipeline/eve_pass.py library/<lane>/heatmaps/<label>.heatmap.json
run_pipeline.py --eve does this for you.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

EVE_HOME = Path(os.environ.get("EVE_HOME", Path.home() / ".local/share/eve"))
EVE_PYTHON = Path(os.environ.get("EVE_PYTHON", Path.home() / ".local/share/eve-venv/bin/python"))


def main(path):
    sys.path.insert(0, str(EVE_HOME))
    import numpy as np
    import torch
    from scipy.spatial import KDTree
    from torch_geometric.data import Data
    from eve_v1 import TriadGATGraphRAG

    torch.manual_seed(0); np.random.seed(0)
    hm = json.loads(Path(path).read_text())
    pts = hm["points"]
    n = len(pts)
    if n < 4:
        raise SystemExit(f"eve needs >= 4 shards, have {n}")
    use = [j for j, d in enumerate(hm["dims"]) if d != "hash_norm"]
    fp = np.array([[p["fingerprint_norm"][j] for j in use] for p in pts], dtype=np.float32)
    fp = fp + np.random.default_rng(0).normal(0, 1e-6, fp.shape).astype(np.float32)  # identical points break KDTree ties

    k = min(4, n - 1)
    tree, edges = KDTree(fp), set()
    for i in range(n):
        for j in tree.query(fp[i], k=k + 1)[1][1:]:
            if i != j:
                edges.add((i, int(j))); edges.add((int(j), i))
    src, dst = zip(*sorted(edges))
    data = Data(x=torch.tensor(fp), edge_index=torch.tensor([src, dst], dtype=torch.long))

    out = 128
    model = TriadGATGraphRAG(in_dim=fp.shape[1], hid=max(32, out // 2), out=out, num_layers=3, heads=4, tau=0.85,
                             num_traces=8, low_k=min(10, n - 2), heat_tau=0.05, lambda_op=0.1)
    model.eval()
    h, g = model.embed_graph(data)          # no no_grad(): the Hessian estimator needs grad
    heat = h.abs().sum(dim=1)
    shatter = torch.norm(h - h.mean(dim=0), dim=1)
    enhanced, retrieved = model.rag_strike(g.squeeze(0), h, g)
    with torch.no_grad():
        _, gsi = model.diffusion_lock(enhanced, torch.tensor(fp))   # needs eve >= 2026-10-12 (diffusion_lock shape fix)
    retrieved = {int(i) for i in (retrieved.tolist() if hasattr(retrieved, "tolist") else retrieved)}
    for i, p in enumerate(pts):
        p["gat_heat"] = round(float(heat[i]), 5)
        p["gat_shatter"] = round(float(shatter[i]), 5)
        p["rag_retrieved"] = i in retrieved
    diag = model.get_triad_diagnostics()
    hm["eve"] = {
        # file hash only — SOURCE.txt names a secret gist, and its id must never reach this public repo
        "source": {"file": "eve_v1.py", "sha256": hashlib.sha256((EVE_HOME / "eve_v1.py").read_bytes()).hexdigest()},
        "gat": {"in_dim": int(fp.shape[1]), "hid": max(32, out // 2), "out": out, "layers": 3, "heads": 4, "seed": 0},
        "nodes": n, "edges": len(edges),
        "gsi_score": round(float(gsi), 6),
        "global_emb_norm": round(float(g.norm()), 6),
        "retrieval_hits": len(retrieved),
        "triad_diagnostics": json.loads(json.dumps(diag, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))),
    }
    Path(path).write_text(json.dumps(hm, indent=2) + "\n")
    print(f"eve: {n} nodes, {len(edges)} edges, GSI {hm['eve']['gsi_score']}, retrieved {len(retrieved)}")


if __name__ == "__main__":
    main(sys.argv[1])
