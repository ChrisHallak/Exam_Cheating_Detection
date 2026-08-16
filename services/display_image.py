import matplotlib.pyplot as plt
from PIL import Image


VIOLATION_LABELS = {
    "MOB": "Mobile Phone",
    "BOK": "Book",
    "NOT": "Notebook / Paper",
    "LAP": "Laptop",
    "TAB": "Tablet",
    "HED": "Headphones",
    "CAL": "Calculator",
    "ABS": "No Person Detected",
    "ADP": "Multiple People Detected",
    "AMB": "Face Not Detected",
    "LFT": "Looking Left",
    "RGT": "Looking Right",
    "UP": "Looking Up",
    "DWN": "Looking Down",
}


def show_frame_with_report(
        frame: Image.Image,
        report: dict
):
    """
    Display a frame together with its analysis report.
    """

    violations = report.get(
        "violations",
        []
    )

    angles = report.get(
        "angles",
        []
    )

    # --------------------------------------------------
    # Create figure
    # --------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 8)
    )

    # Display image
    ax.imshow(frame)

    ax.axis("off")

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    if violations:

        status = "⚠  VIOLATION DETECTED"
        status_color = "#DC2626"

    else:

        status = "✓  NO VIOLATIONS"
        status_color = "#16A34A"

    # --------------------------------------------------
    # Build report text
    # --------------------------------------------------

    report_lines = []

    # Status
    report_lines.append(status)
    report_lines.append("")

    # Violations section
    report_lines.append("VIOLATIONS")
    report_lines.append("──────────────")

    if violations:

        for violation in violations:

            label = VIOLATION_LABELS.get(
                violation,
                violation
            )

            report_lines.append(
                f"●  {label}"
            )

    else:

        report_lines.append(
            "✓  No suspicious activity"
        )

    # Head pose section
    report_lines.append("")
    report_lines.append("HEAD POSE")
    report_lines.append("──────────────")

    if len(angles) >= 2:

        pitch = angles[0]
        yaw = angles[1]

        report_lines.append(
            f"Pitch    {pitch:.1f}°"
        )

        report_lines.append(
            f"Yaw      {yaw:.1f}°"
        )

        if len(angles) >= 3:

            roll = angles[2]

            report_lines.append(
                f"Roll     {roll:.1f}°"
            )

    else:

        report_lines.append(
            "Head pose unavailable"
        )

    # --------------------------------------------------
    # Report box
    # --------------------------------------------------

    ax.text(
        0.03,
        0.97,
        "\n".join(report_lines),
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=14,
        fontweight="bold",
        color="white",
        linespacing=1.5,
        bbox=dict(
            boxstyle="round,pad=0.8",
            facecolor="#111827",
            edgecolor=status_color,
            linewidth=3,
            alpha=0.92
        )
    )

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    ax.set_title(
        "AI Exam Proctoring",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    plt.tight_layout()

    plt.show()