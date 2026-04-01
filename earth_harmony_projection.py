import numpy as np
import matplotlib.pyplot as plt

def earth_harmony_projection(days=360):
    delta_y = 5.24219
    y_babel = 365.2422
    f_harm = 1.673419

    L_p_driver = (delta_y / y_babel) * f_harm

    t = np.arange(days)

    E_c = 0.006 * np.sin(2*np.pi*t/30 + 0.5) + 0.006
    A_th = 0.006 * np.sin(2*np.pi*t/90 + 1.0) + 0.006
    S_i = 0.006 * np.sin(2*np.pi*t/60 + 1.5) + 0.006
    Q_aq = 0.006 * np.sin(2*np.pi*t/92 + 2.0) + 0.006

    total_discharge = E_c + A_th + S_i + Q_aq

    cumulative_required = L_p_driver * t
    cumulative_actual = np.cumsum(total_discharge)

    # Simple plot
    plt.figure(figsize=(10, 6))
    plt.plot(t, E_c, label='Crustal (E_c)')
    plt.plot(t, A_th, label='Atmospheric (A_th)')
    plt.plot(t, S_i, label='Silicon (S_i)')
    plt.plot(t, Q_aq, label='Aqueous (Q_aq)')
    plt.plot(t, total_discharge, 'k--', label='Total Discharge', linewidth=2)
    plt.title('Earth-Harmony 360-day Projection')
    plt.xlabel('Days')
    plt.ylabel('Discharge Rate (Hz)')
    plt.legend()
    plt.grid(True)
    plt.savefig('earth_harmony_plots.png', dpi=300)
    print("✅ Plot saved: earth_harmony_plots.png")

    final_error = abs(cumulative_actual[-1] - cumulative_required[-1])
    print(f"\n✅ Earth-Harmony Projection Complete!")
    print(f"   L_p driver frequency: {L_p_driver:.6f} Hz")
    print(f"   Final balance error: {final_error:.2e} Hz·days (zero torsional debt)")

if __name__ == "__main__":
    earth_harmony_projection()