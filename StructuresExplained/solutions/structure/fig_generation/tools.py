def plot_arrow(subplot, reaction_force, vector_data):
    h = vector_data[0]
    scale = vector_data[1]
    x = vector_data[2][0]
    y = vector_data[2][1]
    len_x = vector_data[2][2]
    len_y = vector_data[2][3]

    subplot.arrow(
        x,
        y,
        len_x,
        len_y,
        head_width=h * 0.15,
        head_length=0.2 * scale,
        ec="b",
        fc="orange",
        zorder=11,
        # head_start_at_zero=head_start_at_zero,
    )

    subplot.text(
        x,
        y,
        f"F={round(abs(reaction_force), 2)}",
        color="k",
        fontsize=9,
        zorder=10,
    )


def plot_moment(subplot, node, reaction_force, vector_data):
    h = vector_data[0]
    if reaction_force > 0:
        subplot.plot(
            node.vertex.x,
            -node.vertex.z,
            marker=r"$\circlearrowleft$",
            ms=25,
            color="orange",
        )
    if reaction_force < 0:
        subplot.plot(
            node.vertex.x,
            -node.vertex.z,
            marker=r"$\circlearrowright$",
            ms=25,
            color="orange",
        )

    subplot.text(
        node.vertex.x + h * 0.2,
        -node.vertex.z + h * 0.2,
        f"R= {round(abs(reaction_force), 2)}",
        color="k",
        fontsize=9,
        zorder=10,
    ),
