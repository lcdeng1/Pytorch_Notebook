import torch
from torch.utils.data import DataLoader
from torch import nn, optim
from torchvision import transforms, datasets
from ae import AE
from vae import VAE
import visdom


def main():
    mnist_train = datasets.MNIST('D:\Projects\Jupyter Notebook\Pytorch\Practice\mnist_data',True, transform=transforms.Compose([
        transforms.ToTensor()
    ]), download=False)
    mnist_train = DataLoader(mnist_train, batch_size=32, shuffle=True)

    mnist_test = datasets.MNIST('D:\Projects\Jupyter Notebook\Pytorch\Practice\mnist_data', False, transform=transforms.Compose([
        transforms.ToTensor()
    ]), download=False)
    mnist_test = DataLoader(mnist_test, batch_size=32, shuffle=True)


    x, _ = next(iter(mnist_train))
    print('x:', x.shape)

    device = torch.device('cuda')
    # model = AE().to(device)
    model = VAE().to(device)
    criteon = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    print(model)

    viz = visdom.Visdom()

    for epoch in range(1000):

        for batchidx, (x, _) in enumerate(mnist_train):
            # [b, 1, 28, 28]
            x = x.to(device)

            # x_hat = model(x)
            x_hat, kld = model(x)
            loss = criteon(x_hat, x)

            if kld is not None:
                elbo = - loss - 1.0 * kld
                loss = - elbo

            # backup
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


        # print(epoch, 'loss:', loss.item())
        print(epoch, 'loss:', loss.item(), 'kld:', kld.item())

        x, _ = iter(mnist_test).next()
        x = x.to(device)
        with torch.no_grad():
            # x_hat = model(x)
            x_hat, _ = model(x)
        viz.images(x, nrow=8, win='x', opts=dict(title='x'))
        viz.images(x_hat, nrow=8, win='x_hat', opts=dict(title='x_hat'))


if __name__ == '__main__':
    main()
