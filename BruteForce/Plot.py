import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import SuperSimpleInitialConditions as ic

class Plot:

    typeLine = ['lime', 'gold', 'darkorange']
    def plotIC(self):

        # отображаем аэродромы вылета в виде точек с подписями
        self.drawPoints(ic.X_q, "Аэр. ", 'go', 10)

        # отображаем кластеры
        self.drawPoints(ic.X_k, "К-р. ", 'ro', 10)

        # отображаем радиусы БЛА тех типов,которые имеются на аэродромах
        for q in range(ic.Q):
            for l in range(ic.L):
                if ic.A_ql[q][l] > 0:
                    self.drawCircle(ic.X_q[q].x, ic.X_q[q].y, ic.R_l[l], self.typeLine[l])
                else:
                    continue

        plt.xlim((-90000, 250000))
        plt.ylim(-100000, 190000)
        plt.ion()
        plt.show()
        plt.pause(0.001)


    def drawPoints(self, points, subscribt, point_property, offset = 10):
        for q in range(len(points)):
            plt.plot([points[q].x], [points[q].y], point_property)
            plt.text(points[q].x + offset, points[q].y + offset, str(subscribt) + str(q + 1))
        plt.grid(True)

    def drawCircle(self, x, y, radius, color):
        circle = plt.Circle((x, y), radius, color=color, fill=False)
        ax = plt.gca()
        ax.add_artist(circle)
