import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import  TextArea, VPacker, HPacker, AnnotationBbox

TO_RAD = np.pi/180
ANG_MULT = 2.0

def get_angles():
    """This could be more sophisticated, but for now is just hardcoded angles"""
    t_c = 30.0  # Cell total
    t_ld = 4.75  # Long drift
    t_sd = 1.7  # Short drift
    t_d = 3.43  # d-mag
    t_f = 10.24  # f-mag

    return t_c, t_ld, t_sd, t_d, t_f



def make_segment(r0, r1, theta_0, theta_1, r_mult=1.0):
    """Returns arrays of r, theta, marking out some segment.
    Pass angles in degrees, to be returned in radians"""
    radii = np.linspace(r0, r1, 100)
    angs = np.linspace(theta_0, theta_1, 100)*TO_RAD*ANG_MULT

    return radii, angs

def make_wedge(r0, r1, theta_0, theta_1):
    """Returns arrays of r, theta, marking out some wedge"""
    r_ins, t_ins = make_segment(r0, r0, theta_0, theta_1)  # Inner border
    r_out, t_out = make_segment(r1, r1, theta_1, theta_0)  # Outer border
    r_lef, t_lef = make_segment(r0, r1, theta_1, theta_1)  # Left hand border
    r_rit, t_rit = make_segment(r1, r0, theta_0, theta_0)  # Right hand border

    rads = np.concatenate([r_ins, r_lef, r_out, r_rit])
    angs = np.concatenate([t_ins, t_lef, t_out, t_rit])


    return rads, angs

def plot_wedge(ax, r0, r1, theta_0, theta_1, col='k', ls='-', lw=2.0, label=''):
    rads, angs = make_wedge(r0, r1, theta_0, theta_1)

    ax.fill(angs, rads, lw=0, color=col, alpha=0.25)
    ax.plot(angs, rads, lw=lw, color=col, ls=ls, label=label)

    # ax.text((theta_0+theta_1)*ANG_MULT*TO_RAD/2, (r0+r1)/2, label, color='k')

def plot_segment(ax, r0, r1, theta_0, theta_1, col='k', ls='-', lw=2.0):
    rads, angs = make_segment(r0, r1, theta_0, theta_1)

    ax.plot(angs, rads, lw=lw, ls=ls, color=col)

def plot_ang_arrow(ax, r, theta_0, theta_1, text='', headsize=0.03):
    head_len = headsize
    plot_segment(ax, r, r, theta_0, theta_1, lw=1.5, col="k", ls='-')  # Line
    plot_segment(ax, r - head_len / 2, r + head_len / 2, theta_0, theta_0, lw=1.5, col="k", ls='-')  # One head
    plot_segment(ax, r - head_len / 2, r + head_len / 2, theta_1, theta_1, lw=1.5, col="k", ls='-')  # Other head

    ax.text((theta_0+theta_1)*ANG_MULT*TO_RAD/2, r+head_len/2, text, color='k')

def plot_rad_arrow(ax, r0, r1, theta, text='', headsize=0.75):
    head_len = headsize
    plot_segment(ax, r0, r1, theta, theta, lw=1.5, col="0.25", ls='-')  # Line
    # plot_segment(ax, r0, r0, theta-head_len/2, theta+head_len/2, lw=1.5, col="k", ls='-')  # One head
    plot_segment(ax, r1, r1, theta, theta+head_len, lw=1.5, col="0.25", ls='-')  # Other head
    ax.text(theta*ANG_MULT*TO_RAD*1.075, r1*1., text, color='k', fontsize=12)

def plot_cell(show=True, save=False):
    """Makes total cell"""

    # Get the angles
    t_c, t_ld, t_sd, t_d, t_f = get_angles()

    # Get the distances - cosmetic
    r0 = 0.3
    r1 = 0.5

    # Define the fig and axes for the graph
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.set_thetamin(0)
    ax.set_thetamax(60)
    ax.grid(axis='y')
    ax.set_title("Layout of KURRI Main Ring", fontsize=16)
    t_ticks = [0, 5, 10, 15, 20, 25, 30]
    plt.xticks(np.array(t_ticks)*TO_RAD*2, [fr'${t}\degree$' for t in t_ticks])
    plt.yticks([])
    ax.set_ylim(0, r1+0.1)

    # Make wedge to contain the entire cell
    #plot_segment(ax, 0, r1+0.1, 0, 0, ls='--', lw=1.5)
    #plot_segment(ax, 0, r1+0.1, t_c, t_c, ls='--', lw=1.5)


    # Make the F and D magnets
    t_d1_start = t_ld
    t_f_start = t_d1_start + t_d + t_sd
    t_d2_start = t_f_start + t_f + t_sd
    plot_wedge(ax, r0, r1, t_d1_start, t_d1_start+t_d, col='royalblue', label='D Magnet')  # First D magnet
    plot_wedge(ax, r0, r1, t_f_start, t_f_start + t_f, col='firebrick', label='F Magnet')  # F magnet
    plot_wedge(ax, r0, r1, t_d2_start, t_d2_start+t_d, col='royalblue')  # Second D magnet

    # Plot arrows to show dimensions
    plot_ang_arrow(ax, 0.1, 0, t_c, r'$\theta_{C}$', headsize=0)
    r_arr = r1+0.025
    plot_ang_arrow(ax, r_arr, 0, t_ld, r'$\theta_{LD}$')
    plot_ang_arrow(ax, r_arr, t_d1_start, t_d1_start+t_d, r'$\theta_{D}$')
    plot_ang_arrow(ax, r_arr, t_d1_start+t_d, t_d1_start+t_d+t_sd, r'$\theta_{SD}$')
    plot_ang_arrow(ax, r_arr, t_f_start, t_f_start+t_f/2, r'$\theta_{F}/2$')

    plot_rad_arrow(ax, 0, r0, t_d2_start+t_d, r'$r_0$')
    plot_rad_arrow(ax, 0, r1, t_d2_start+t_d, r'$r_1$')

    # Write in the values of angles and lengths using artists
    text = [fr'$\theta_C$',
            fr'$\theta_{"{LD}"}$',
            fr'$\theta_D$',
            fr'$\theta_{"{SD}"}$',
            fr'$\theta_F$']
    val = [rf'$= {v}\degree$' for v in [t_c, t_ld, t_d, t_sd, t_f]]
    Texts = [TextArea(t) for t in text]
    Vals = [TextArea(v) for v in val]
    textbox = VPacker(children=Texts, pad=0.1, sep=0.1)
    valsbox = VPacker(children=Vals, pad=0.1, sep=2.4)  # This 'sep' is fine-tuned to make boxes align!
    totbox = HPacker(children=[textbox, valsbox], pad=0.1, sep=0.1)
    ann = AnnotationBbox(totbox, (0.05, 0.8), xycoords=ax.transAxes,
                         box_alignment=(0.05, 0.8),
                         bboxprops=dict(facecolor='wheat', boxstyle='round', color='black'))
    ann.set_figure(fig)
    fig.artists.append(ann)

    text2 = [r'$r_0$', r'$r_1$']
    val2 = [r'$= 4.3$m', r'$= 5.4$m']
    Texts2 = [TextArea(t) for t in text2]
    Vals2 = [TextArea(v) for v in val2]
    textbox2 = VPacker(children=Texts2, pad=0.1, sep=0.1)
    valsbox2 = VPacker(children=Vals2, pad=0.1, sep=1)  # This 'sep' is fine-tuned to make boxes align!
    totbox2 = HPacker(children=[textbox2, valsbox2], pad=0.1, sep=0.1)
    ann2 = AnnotationBbox(totbox2, (0.05, 0.5), xycoords=ax.transAxes,
                          box_alignment=(0.05, 0.5),
                          bboxprops=dict(facecolor='wheat', boxstyle='round', color='black'))
    ann2.set_figure(fig)
    fig.artists.append(ann2)

    # Legend
    ax.legend(loc=(0.75, 0.8), facecolor='lavenderblush', edgecolor='k')

    #Misc
    fig.tight_layout()
    if save:
        fig.savefig('figs/KURRI_layout.png')
        fig.savefig('figs/KURRI_layout.pdf')
    if show:
        fig.show()

if __name__ == '__main__':
    plot_cell(show=True, save=True)
