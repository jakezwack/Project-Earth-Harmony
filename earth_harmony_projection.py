import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def earth_harmony_projection(days=360, save_plots=True):
    """
    Extended Earth-Harmony Projection with Starlink Orbital Resonance
    """
    # Core Constants
    delta_y = 5.24219
    y_babel = 365.2422
    f_harm = 1.673419

    L_p_driver = (delta_y / y_babel) * f_harm

    t = np.arange(days)

    # Original 4 fluxes
    E_c = 0.006 * np.sin(2*np.pi*t/30 + 0.5) + 0.006   # Crustal
    A_th = 0.006 * np.sin(2*np.pi*t/90 + 1.0) + 0.006   # Atmospheric
    S_i = 0.006 * np.sin(2*np.pi*t/60 + 1.5) + 0.006    # Silicon
    Q_aq = 0.006 * np.sin(2*np.pi*t/92 + 2.0) + 0.006   # Aqueous

    # NEW: Starlink Orbital Resonance (9.97 s Master Shutter)
    Starlink = 0.006 * np.sin(2*np.pi*t/9.97 + 2.5) + 0.006

    total_discharge = E_c + A_th + S_i + Q_aq + Starlink

    cumulative_required = L_p_driver * t
    cumulative_actual = np.cumsum(total_discharge)

    if save_plots:
        fig = plt.figure(figsize=(14, 10))

        # Plot 1: Daily Discharge Rates
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(t, E_c, label='$E_c$ (Crustal)', alpha=0.8)
        ax1.plot(t, A_th, label='$A_{th}$ (Atmospheric)', alpha=0.8)
        ax1.plot(t, S_i, label='$S_i$ (Silicon)', alpha=0.8)
        ax1.plot(t, Q_aq, label='$Q_{aq}$ (Aqueous)', alpha=0.8)
        ax1.plot(t, Starlink, label='Starlink (Orbital)', alpha=0.8, color='purple')
        ax1.plot(t, total_discharge, 'k--', label='Total Discharge', linewidth=2)
        ax1.set_title('Daily Discharge Rates - with Starlink Resonance')
        ax1.set_xlabel('Days')
        ax1.set_ylabel('Rate (Hz)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Cumulative Balance
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(t, cumulative_required, 'r-', label='Required Balance')
        ax2.plot(t, cumulative_actual, 'b-', label='Actual Cumulative')
        ax2.set_title('Cumulative Energy Balance')
        ax2.set_xlabel('Days')
        ax2.set_ylabel('Cumulative Energy (Hz·days)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Plot 3: Contribution Breakdown
        ax3 = fig.add_subplot(2, 2, 3)
        contributions = [np.sum(E_c), np.sum(A_th), np.sum(S_i), np.sum(Q_aq), np.sum(Starlink)]
        labels = ['$E_c$', '$A_{th}$', '$S_i$', '$Q_{aq}$', 'Starlink']
        ax3.pie(contributions, labels=labels, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Total Contribution by Term')

        # Plot 4: Heatmap
        ax4 = fig.add_subplot(2, 2, 4)
        data = np.vstack([E_c, A_th, S_i, Q_aq, Starlink])
        im = ax4.imshow(data, aspect='auto', cmap='viridis')
        ax4.set_yticks([0,1,2,3,4])
        ax4.set_yticklabels(labels)
        ax4.set_title('4D Circuit Heatmap with Starlink')
        ax4.set_xlabel('Days')
        plt.colorbar(im, ax=ax4, label='Discharge Rate (Hz)')

        plt.tight_layout()
        plt.savefig('earth_harmony_plots.png', dpi=300, bbox_inches='tight')
        print("✅ Extended plot saved: earth_harmony_plots.png")

        with PdfPages('earth_harmony_figures.pdf') as pdf:
            pdf.savefig(fig)
        print("✅ PDF saved: earth_harmony_figures.pdf")

    final_error = abs(cumulative_actual[-1] - cumulative_required[-1])
    print(f"\n✅ Extended Earth-Harmony Projection Complete!")
    print(f"   L_p driver frequency: {L_p_driver:.6f} Hz")
    print(f"   Final balance error: {final_error:.2e} Hz·days")

    return L_p_driver, final_error


if __name__ == "__main__":
    earth_harmony_projection()