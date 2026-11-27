"""Plot RMSD, RMSF and radius of gyration from GROMACS .xvg files."""
import numpy as np
import matplotlib.pyplot as plt

def load_xvg(path):
    """Read a GROMACS .xvg file and skip comment lines (# and @)."""
    with open(path) as f:
        rows = [line for line in f if not line.startswith(("#", "@"))]
    return np.loadtxt(rows)

# ---- RMSD: structural change over time ----
rmsd = load_xvg("analysis/rmsd.xvg")
plt.figure(figsize=(6, 3.5))
plt.plot(rmsd[:, 0], rmsd[:, 1])
plt.xlabel("Time (ns)"); plt.ylabel("Backbone RMSD (nm)")
plt.title("Lysozyme backbone RMSD")
plt.tight_layout(); plt.savefig("plots/rmsd.png", dpi=150)

# ---- RMSF: flexibility per residue ----
rmsf = load_xvg("analysis/rmsf.xvg")
plt.figure(figsize=(6, 3.5))
plt.plot(rmsf[:, 0], rmsf[:, 1])
plt.xlabel("Residue"); plt.ylabel("C-alpha RMSF (nm)")
plt.title("Lysozyme residue flexibility")
plt.tight_layout(); plt.savefig("plots/rmsf.png", dpi=150)

# ---- Radius of gyration: compactness over time ----
rg = load_xvg("analysis/gyrate.xvg")
plt.figure(figsize=(6, 3.5))
plt.plot(rg[:, 0], rg[:, 1])
plt.xlabel("Time (ps)"); plt.ylabel("Radius of gyration (nm)")
plt.title("Lysozyme radius of gyration")
plt.tight_layout(); plt.savefig("plots/gyrate.png", dpi=150)

# ---- Key numbers for the README ----
print(f"RMSD: mean over last half = {rmsd[len(rmsd)//2:, 1].mean():.3f} nm")
print(f"Rg:   mean = {rg[:, 1].mean():.3f} nm, std = {rg[:, 1].std():.3f} nm")
top = rmsf[np.argsort(rmsf[:, 1])[-5:][::-1]]
print("Most flexible residues (residue, RMSF nm):")
for res, val in top:
    print(f"  {int(res):4d}  {val:.3f}")
