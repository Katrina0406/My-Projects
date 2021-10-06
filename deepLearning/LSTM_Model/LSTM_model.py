
import torch
from torch.nn import Module, LSTM, Linear
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

class Net(Module):

    def __init__(self, config):
        super(Net, self).__init__()
        self.lstm = LSTM(input_size=config.input_size, hidden_size=config.hidden_size,
                         num_layers=config.lstm_layers, batch_first=True, dropout=config.dropout_rate)
        self.linear = Linear(in_features=config.hidden_size, out_features=config.output_size)

    def forward(self, x, hidden=None):
        lstm_out, hidden = self.lstm(x, hidden)
        linear_out = self.linear(lstm_out)
        return linear_out, hidden


def train(config, logger, train_and_valid_data):
    if config.do_train_visualized:
        import visdom
        vis = visdom.Visdom(env='model_pytorch')

    train_X, train_Y, valid_X, valid_Y = train_and_valid_data
    train_X, train_Y = torch.from_numpy(train_X).float(), torch.from_numpy(train_Y).float()     # change to Tensor
    train_loader = DataLoader(TensorDataset(train_X, train_Y), batch_size=config.batch_size)    # DataLoader automatically generates trainable batch data
    valid_X, valid_Y = torch.from_numpy(valid_X).float(), torch.from_numpy(valid_Y).float()
    valid_loader = DataLoader(TensorDataset(valid_X, valid_Y), batch_size=config.batch_size)

    device = torch.device("cuda:0" if config.use_cuda and torch.cuda.is_available() else "cpu") # CPU or GPU to train
    model = Net(config).to(device)      # if train on GPU， .to(device) will copy model/data to GPU
    if config.add_train:                # if add_train，will load previous model's params first
        model.load_state_dict(torch.load(config.model_save_path + config.model_name))
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = torch.nn.MSELoss()      # define optimizer and loss

    valid_loss_min = float("inf")
    bad_epoch = 0
    global_step = 0
    for epoch in range(config.epoch):
        logger.info("Epoch {}/{}".format(epoch, config.epoch))
        model.train()                   # in pytorch，turn to train mode
        train_loss_array = []
        hidden_train = None
        for i, _data in enumerate(train_loader):
            _train_X, _train_Y = _data[0].to(device),_data[1].to(device)
            optimizer.zero_grad()               # gradient = 0
            pred_Y, hidden_train = model(_train_X, hidden_train)    # forward function

            if not config.do_continue_train:
                hidden_train = None             # non-continuous training，reset hidden value
            else:
                h_0, c_0 = hidden_train
                h_0.detach_(), c_0.detach_()    # eliminate gradient info
                hidden_train = (h_0, c_0)
            loss = criterion(pred_Y, _train_Y)  # calculate loss
            loss.backward()                     # spread loss backwards
            optimizer.step()                    # update params with optimizer
            train_loss_array.append(loss.item())
            global_step += 1
            if config.do_train_visualized and global_step % 100 == 0:   # show every 100 steps
                vis.line(X=np.array([global_step]), Y=np.array([loss.item()]), win='Train_Loss',
                         update='append' if global_step > 0 else None, name='Train', opts=dict(showlegend=True))

        # The early stopping mechanism - when the model training for consecutive config.patience epochs does not 
        # improve the prediction effect of the validation set, it stops to prevent over-fitting
        model.eval()                    # in pytorch，turn to predict mode
        valid_loss_array = []
        hidden_valid = None
        for _valid_X, _valid_Y in valid_loader:
            _valid_X, _valid_Y = _valid_X.to(device), _valid_Y.to(device)
            pred_Y, hidden_valid = model(_valid_X, hidden_valid)
            if not config.do_continue_train: hidden_valid = None
            loss = criterion(pred_Y, _valid_Y)  
            valid_loss_array.append(loss.item())

        train_loss_cur = np.mean(train_loss_array)
        valid_loss_cur = np.mean(valid_loss_array)
        logger.info("The train loss is {:.6f}. ".format(train_loss_cur) +
              "The valid loss is {:.6f}.".format(valid_loss_cur))
        if config.do_train_visualized:      # the first train_loss_cur is so large that it doens't display in visdom
            vis.line(X=np.array([epoch]), Y=np.array([train_loss_cur]), win='Epoch_Loss',
                     update='append' if epoch > 0 else None, name='Train', opts=dict(showlegend=True))
            vis.line(X=np.array([epoch]), Y=np.array([valid_loss_cur]), win='Epoch_Loss',
                     update='append' if epoch > 0 else None, name='Eval', opts=dict(showlegend=True))

        if valid_loss_cur < valid_loss_min:
            valid_loss_min = valid_loss_cur
            bad_epoch = 0
            torch.save(model.state_dict(), config.model_save_path + config.model_name)  # save model
        else:
            bad_epoch += 1
            if bad_epoch >= config.patience:    # If the validation set index does not improve for consecutive patience epochs, stop training
                logger.info(" The training stops early in epoch {}".format(epoch))
                break


def predict(config, test_X):
    # get prediction data
    test_X = torch.from_numpy(test_X).float()
    test_set = TensorDataset(test_X)
    test_loader = DataLoader(test_set, batch_size=1)

    # load model
    device = torch.device("cuda:0" if config.use_cuda and torch.cuda.is_available() else "cpu")
    model = Net(config).to(device)
    model.load_state_dict(torch.load(config.model_save_path + config.model_name))   # load model params

    # define a tensor to save predicting results
    result = torch.Tensor().to(device)

    # prediction
    model.eval()
    hidden_predict = None
    for _data in test_loader:
        data_X = _data[0].to(device)
        pred_X, hidden_predict = model(data_X, hidden_predict)
        # if not config.do_continue_train: hidden_predict = None  # regardless of whether continuous training mode, it;s better to pass hidden of previous time_step to next one
        cur_pred = torch.squeeze(pred_X, dim=0)
        result = torch.cat((result, cur_pred), dim=0)

    return result.detach().cpu().numpy()    # elininare gradient info first，return numpy data in the end
