
import json
import matplotlib.pyplot as plt


def show_metrics(results, method):
    
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))
    fig.suptitle(method, fontsize=16)

    result = [float(image[0]) for image in results]
    axs[0].plot(result)
    axs[0].set_ylim([0, 100])
    axs[0].grid(color='r', linestyle='-', linewidth=1)
    axs[0].set_xticks(range(0, len(result), 5))
    axs[0].set_title('PSNR')

    result = [float(image[1]) for image in results]
    axs[1].plot(result, 'tab:orange')
    axs[1].set_title('SSIM')
    axs[1].set_ylim([0, 1])
    axs[1].grid(color='r', linestyle='-', linewidth=1)
    axs[1].set_xticks(range(0, len(result), 5))

    # plt.show()
    plt.savefig(method + '.png')



def main(path):
    plt.switch_backend('agg')

    methods = [
        'nlmp.json',
        'DCTdenoising.json'
    ]

    results = []

    for method_file in methods:
        with open(path + method_file) as f:
            data = json.load(f)

            data = data['results']

            output = []

            for img in data:
                output.append((img['PSNR'], img['SSIM'], img['image_file']))

            results = sorted(output,  key=lambda x: x[2])
            
            show_metrics(results, method_file)

    print('done')


if __name__ == '__main__':
    path = '../result_metadata/'
    main(path)