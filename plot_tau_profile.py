import numpy as np
import matplotlib.pyplot as plt
from getdist.types import BestFit
from run_tau_profile import taus,taufn

chi2   = np.empty_like(taus)
omegam = np.empty_like(taus)

for i, tau in enumerate(taus):
    prefix = taufn(tau)
    bf = BestFit(prefix + ".minimum")
    chi2[i] = 2 * bf.logLike
    omegam[i] = bf.parWithName("OmegaM").best_fit

dchi2 = chi2 - chi2.min()

# quick table
print(f"{'tau':>6} {'chi2':>14} {'dchi2':>10} {'OmegaM':>10}")
for t, c, d, om in zip(taus, chi2, dchi2, omegam):
    print(f"{t:6.3f} {c:14.4f} {d:10.4f} {om:10.4f}")
print(f"\nMinimum chi2 at tau = {taus[np.argmin(chi2)]:.3f}")

# plot
fig, ax = plt.subplots(figsize=(6.5, 4.5))
# left axis: dchi2
l1, = ax.plot(taus, dchi2, "o-", color="C0", label=r"$\Delta\chi^2$")
ax.axhline(1, ls=":", color="gray", lw=1)
ax.axhline(4, ls=":", color="gray", lw=1)
ax.text(taus[-1], 1.05, r"$1\sigma$", color="gray", va="bottom", ha="right")
ax.text(taus[-1], 4.05, r"$2\sigma$", color="gray", va="bottom", ha="right")
ax.set_xlabel(r"$\tau$")
ax.set_ylabel(r"$\Delta\chi^2(\tau)$", color="C0")
ax.tick_params(axis="y", labelcolor="C0")
ax.grid(alpha=0.3)
# right axis: best-fit OmegaM
ax2 = ax.twinx()
l2, = ax2.plot(taus, omegam, "s--", color="C3", label=r"$\Omega_{\rm m}$")
ax2.set_ylabel(r"$\Omega_{\rm m}$", color="C3")
ax2.tick_params(axis="y", labelcolor="C3")
# unified legend
ax.legend(handles=[l1, l2], loc="best", frameon=False)
plt.tight_layout()
plt.title(r'CMB 2pt: Planck PR4 ($30<\ell<1000$) + ACT DR6 ($\ell>1000$) + SPT-3G D1')
plt.savefig("tau_profile.pdf", bbox_inches="tight")