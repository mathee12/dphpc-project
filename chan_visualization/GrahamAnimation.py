"""
Class which defines the functionality to plot a graham scan.

Need to pass a data_dict to the constructor which we get using the DataLoader class.
"""
from matplotlib.pyplot import cm
import numpy as np


class GrahamAnimation:
    def __init__(self, data_dict):
        """
            - state represents the 3 indices of base_idx, last_idx, last_idx - 1, used to draw the arrows
            - hull_points is the stack of points that lie on the hull (at a given moment)
        """

        self.all_points         = data_dict['sub_sorted']
        self.final_sub_hulls    = data_dict['hull_points']
        self.graham_run         = data_dict['graham_runs']
        self.n_graham_subs      = data_dict['n_graham_subs']

        self.curr_sub_hull      = {idx: {'x': [self.all_points[idx]['x'][add_idx] for add_idx in [-1, 0, 1]],
                                         'y': [self.all_points[idx]['y'][add_idx] for add_idx in [-1, 0, 1]]}
                                   for idx in range(self.n_graham_subs)}

        self.state              = {idx: [] for idx in range(self.n_graham_subs)}
        self.curr_orientation   = {idx: None for idx in range(self.n_graham_subs)}
        self.n_steps            = {idx: len(self.graham_run[idx]) for idx in range(self.n_graham_subs)}
        self.two_lines          = {idx: None for idx in range(self.n_graham_subs)}
        self.hull_lines         = {idx: None for idx in range(self.n_graham_subs)}

        self.two_lines_color    = {'clockwise': 'black', 'anticlockwise': 'green'}
        self.step               = 0
        self.ax                 = None

        self.colors             = cm.rainbow(np.linspace(0, 1, self.n_graham_subs))

        # self.idx_stack = [len(self.all_points['x']) - 1, 0, 1]  # unused

    # not used at the moment
    def update_stack_state(self, step):

        add_rem_flag = self.graham_run[step][1]

        if add_rem_flag == 1:
            self.idx_stack.append(self.graham_run[step][0])
        elif add_rem_flag == -1:
            del self.idx_stack[-2]

    def update_graham_state(self, step, idx):
        self.state[idx] = self.graham_run[idx][step][:6]

        for i, item in enumerate(self.state):
            if item < 0:
                self.state[i] = 0

        add_point = self.graham_run[idx][step][6]

        add_rem_x = self.graham_run[idx][step][7]
        add_rem_y = self.graham_run[idx][step][8]

        if add_point:
            self.curr_sub_hull[idx]['x'].append(add_rem_x)
            self.curr_sub_hull[idx]['y'].append(add_rem_y)
        else:
            self.curr_sub_hull[idx]['x'].remove(add_rem_x)
            self.curr_sub_hull[idx]['y'].remove(add_rem_y)

        orientation = self.graham_run[idx][step][9]
        if orientation == -1:
            self.curr_orientation[idx] = 'clockwise'
        elif orientation == 1:
            self.curr_orientation[idx] = 'anticlockwise'

    def get_two_lines_pos(self, idx):
        # x = [self.all_points['x'][idx] for idx in self.idx_stack[-3:]]
        # y = [self.all_points['y'][idx] for idx in self.idx_stack[-3:]]
        x = self.state[idx][0: 3]
        y = self.state[idx][3: 6]
        return x, y

    def get_hull_lines_pos(self, idx):
        # x = [self.all_points['x'][idx] for idx in self.idx_stack]
        # y = [self.all_points['y'][idx] for idx in self.idx_stack]
        x = self.curr_sub_hull[idx]['x']
        y = self.curr_sub_hull[idx]['y']
        return x, y

    def plot_all_points(self):
        # TODO: animation of quick sort, means adding points one after the other

        for idx in range(self.n_graham_subs):
            hull_color = self.colors[idx]
            points_color = self.colors[idx]
            self.ax.scatter(self.all_points[idx]['x'], self.all_points[idx]['y'], s=20, c=points_color, alpha=0.8, edgecolors='none')
            self.ax.scatter(self.final_sub_hulls[idx]['x'], self.final_sub_hulls[idx]['y'], s=20, c=hull_color, alpha=0.8, edgecolors='none')

            self.ax.plot(self.final_sub_hulls[idx]['x'], self.final_sub_hulls[idx]['y'], c=hull_color, alpha=0.8, linewidth=0.4)
            self.ax.plot([self.final_sub_hulls[idx]['x'][0], self.final_sub_hulls[idx]['x'][-1]],
                         [self.final_sub_hulls[idx]['y'][0], self.final_sub_hulls[idx]['y'][-1]], c=hull_color, alpha=0.8, linewidth=0.4)

        ''' Outcomment to label points '''
        # for idx in range(len(self.all_points['x'])):
        #    self.ax.text(self.all_points['x'][idx], self.all_points['y'][idx], str(idx))

        self.ax.axis('off')

    def set_ax(self, ax):
        self.ax = ax

    def init_animation(self):

        for idx in range(self.n_graham_subs):
            hull_color = self.colors[idx]
            self.two_lines[idx], = self.ax.plot([], [], c=hull_color, alpha=0.8, linewidth=3)  # switching red / cyan
            self.hull_lines[idx], = self.ax.plot([], [], c=hull_color, alpha=0.8, linewidth=3)
        
        return tuple(self.two_lines) + tuple(self.hull_lines)

    def animate(self, step):
        for idx in range(self.n_graham_subs):
            if 0 < step < self.n_steps[idx]:
                self.update_graham_state(step, idx)
                self.two_lines[idx].set_data(*self.get_two_lines_pos(idx))
                self.two_lines[idx].set_color(self.two_lines_color[self.curr_orientation[idx]])
                self.hull_lines[idx].set_data(*self.get_hull_lines_pos(idx))
        
        return tuple(self.two_lines) + tuple(self.hull_lines)

