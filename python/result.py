#Class used for ploting the final result out of the simulation
#the magnitudes ploted are Step Temp Epot Ekin Etot

class Result(object):

    def __init__(self, time, temp, Ekin, Epot, Etot):
        self.time = time
        self.temp = temp
        self.Ekin = Ekin
        self.Epot = Epot
        self.Etot = Etot

    def graph(self):
        import matplotlib.pyplot as plt
        fig, (ax0, ax1) = plt.subplots(nrows=2)

        ax0.plot(self.time, self.temp)
        ax0.set_title('Temp vs Time')
        ax0.set_xlabel('Time')
        ax0.set_ylabel('Temp')

        ax1.plot(self.time, self.Ekin, label = 'Kinetic')
        ax1.plot(self.time, self.Epot, label = 'Potential')
        ax1.plot(self.time, self.Etot, label = 'Total')

        ax1.legend(loc='upper right')

        ax1.set_title('Energy vs Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Energy')

        plt.subplots_adjust(hspace=0.5)

        plt.show()
