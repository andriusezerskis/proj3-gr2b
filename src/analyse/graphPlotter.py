import numpy as np
from matplotlib import pyplot as plt


class GraphPlotter:

    @staticmethod
    def plot_scores(scores_to_plot, keys, entity_type, save=False, path="datas/res.png"):
        plt.figure(figsize=(12, 6))

        for key in keys.keys():
            scores_array = np.array(scores_to_plot[key])
            step = np.arange(scores_array.shape[1])

            mean_scores = np.mean(scores_to_plot[key], axis=0)
            std_deviation = np.std(scores_to_plot[key], axis=0)

            plt.fill_between(step[:len(mean_scores)], mean_scores - std_deviation, mean_scores + std_deviation,
                             color=keys[key][1])
            plt.plot(step[:len(mean_scores)], mean_scores, label=key, color=keys[key][0])

        plt.title(f"Évolution des populations {entity_type}")
        plt.xlabel('Heures')
        plt.ylabel('Population moyenne')
        plt.legend()
        plt.grid()

        if save:
            plt.savefig(path)
        plt.show()


def summarize_data(n=10):
    samples = {}
    for i in range(1, n+1):
        with open(f"datas/evolution{""}.txt", 'r') as f:
            res = eval(f.read())
            for key in res.keys():
                if i == 1:
                    samples[key] = [res[key][1:]]
                else:
                    samples[key].append(res[key][1:])
    return samples

def print_data(summarized):
    for key in summarized.keys():
        print(f"{key}")
        for e in summarized[key]:
            print(f"{len(e)}, {e}")
        print("\n")


if __name__ == '__main__':
    i = 2
    summarized = summarize_data()
    print_data(summarized)
    save = True
    #GraphPlotter.plot_scores(summarized, {"Humain": ["#00B7BB", "#9ECDC6"], "Crabe": ["#EA9300", "#DEBE8A"], "Arbre": ["#4F8F00", "#BDCFA4"]}, "terrestre", save, path="datas/terrestre.png")
    #GraphPlotter.plot_scores(summarized, {"Leopard des neiges": ["#BB133E", "#C59997"], "Chevre": ["#00B7BB", "#9ECDC6"], "Fleur": ["#4F8F00", "#BDCFA4"]}, "alpestre", save, path="datas/alpestre.png")
    #GraphPlotter.plot_scores(summarized, {"Crabe": ["#EA9300", "#DEBE8A"], "Poisson": ["#00B7BB", "#9ECDC6"], "Algue": ["#4F8F00", "#BDCFA4"]}, "marines", save, path="datas/marines.png")
    GraphPlotter.plot_scores(summarized, {
                                          "Humain": ["#FCBF00", "#FCE086"],
                                          "Crabe": ["#EA9300", "#DEBE8A"],
                                          "Arbre": ["#4F8F00", "#BDCFA4"],
                                          "Leopard des neiges": ["#797979", "#D6D6D6"],
                                          "Chevre": ["#9B41CA", "#AE97C3"],
                                          "Fleur": ["#BB133E", "#C59997"],
                                          "Poisson": ["#00B7BB", "#9ECDC6"],
                                          "Algue": ["#004D80", "#AEBBD4"]
                                          }, "", save, path="datas/graphe/all.png")