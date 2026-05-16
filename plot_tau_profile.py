import argparse
import numpy as np
import matplotlib.pyplot as plt
from getdist.types import BestFit
from run_tau_profile import taus

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        help="Base config name (with or without .yaml extension), e.g. cmb2pt_lite",
    )
    args = parser.parse_args()

    stem = args.config[:-5] if args.config.endswith(".yaml") else args.config
    taufn = lambda tau: f"chains/{stem}_tau={tau:.2f}"

    # load minima, skipping any tau whose minimization didn't finish / didn't write a usable file
    taus_used, chi2_used, omegam_used = [], [], []
    for tau in taus:
        prefix = taufn(tau)
        try:
            bf = BestFit(prefix + ".minimum")
            c = 2 * bf.logLike
            om = bf.parWithName("OmegaM").best_fit
        except Exception as e:
            print(f"  skipping tau={tau:.3f}: {type(e).__name__}: {e}")
            continue
        taus_used.append(tau)
        chi2_used.append(c)
        omegam_used.append(om)

    if not taus_used:
        raise SystemExit(f"No usable .minimum files found for config '{stem}'.")

    taus_arr   = np.array(taus_used)
    chi2_arr   = np.array(chi2_used)
    omegam_arr = np.array(omegam_used)
    dchi2      = chi2_arr - chi2_arr.min()

    # table
    print(f"\n{'tau':>6} {'chi2':>14} {'dchi2':>10} {'OmegaM':>10}")
    for t, c, d, om in zip(taus_arr, chi2_arr, dchi2, omegam_arr):
        print(f"{t:6.3f} {c:14.4f} {d:10.4f} {om:10.4f}")
    print(f"\nMinimum chi2 at tau = {taus_arr[np.argmin(chi2_arr)]:.3f}")

    # plot
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    l1, = ax.plot(taus_arr, dchi2, "o-", color="C0", label=r"$\Delta\chi^2$")
    ax.axhline(1, ls=":", color="gray", lw=1)
    ax.axhline(4, ls=":", color="gray", lw=1)
    ax.text(taus_arr[-1], 1.05, r"$1\sigma$", color="gray", va="bottom", ha="right")
    ax.text(taus_arr[-1], 4.05, r"$2\sigma$", color="gray", va="bottom", ha="right")
    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel(r"$\Delta\chi^2(\tau)$", color="C0")
    ax.tick_params(axis="y", labelcolor="C0")
    ax.grid(alpha=0.3)

    ax2 = ax.twinx()
    l2, = ax2.plot(taus_arr, omegam_arr, "s--", color="C3", label=r"$\Omega_{\rm m}$")
    ax2.set_ylabel(r"$\Omega_{\rm m}$", color="C3")
    ax2.tick_params(axis="y", labelcolor="C3")

    ax.legend(handles=[l1, l2], loc="best", frameon=False)
    plt.title(rf"CMB 2pt: {stem}")
    plt.tight_layout()
    outpath = f"tau_profile_{stem}.pdf"
    plt.savefig(outpath, bbox_inches="tight")
    print(f"\nSaved {outpath}")