# -*- coding: utf-8 -*-
"""LSTM_Prediction.ipynb

This one is for trainning data. We will split training and validation sets inside of it.Leave test data for testing in the end.
after you get Xtrain and ytrain -->
First create a model: model = LSTM()
then train: model = train_lstm(model,Xtrain,ytrain)
"""

import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class LSTM(nn.Module):
    def __init__(self, input_dim=47, hidden_dim=100, num_layers=3, output_dim=1):
        super(LSTM, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.num_layers = num_layers
        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        # Readout layer
        self.fc1 = nn.Linear(hidden_dim, output_dim)
  

    def forward(self, x):
        # print("x shape:",x.shape)
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        # Initialize cell state
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        # print("h0",h0.shape)
        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        # print("lstm out:",out.shape)
        # print("out[:, -1, :]:",out[:, -1, :].shape)
        # Index hidden state of last time step
        # out[:, -1, :] --> just want last time step hidden states! 
        # or else will return 49 days of hidden states
        out = self.fc1(out[:, -1, :])
        # print("final out:",out.shape)
        return out

def train_lstm(model, Xtrain, ytrain, val_size = 0.2, num_epochs=200, window_size=49, viz_result = True):
  
  x_train = torch.from_numpy(Xtrain).type(torch.Tensor)
  y_train = torch.from_numpy(ytrain).type(torch.Tensor)
  
  loss_fn = torch.nn.MSELoss()
  optimiser = torch.optim.Adam(model.parameters(), lr=0.001)
  hist = np.zeros(num_epochs)
  hist_val = np.zeros(num_epochs)
  best_val = 1000
  for t in range(num_epochs):
      # Initialise hidden state
      # Don't do this if you want your LSTM to be stateful
      # model.hidden = model.init_hidden()
      # Forward pass
      y_train_pred = model(x_train[:-len(x_train)*val_size])
      loss = loss_fn(y_train_pred, y_train_sc[:-len(x_train)*val_size])
      # Zero out gradient, else they will accumulate between epochs
      optimiser.zero_grad()
      # Backward pass
      loss.backward()
      # Update parameters
      optimiser.step()
      # if t % 10 == 0 and t !=0:
      model.eval()
      y_val_pred = model(x_train[-len(x_train)*val_size:])
      loss_val = loss_fn(y_val_pred, y_train_sc[-len(x_train)*val_size:])
      print("Epoch", t+1, "Training MSE: {:.4f}".format(loss.item()),
            "Val MSE: {:.4f}".format(loss_val.item()))
      # print()
      hist[t] = loss.item()
      hist_val[t] = loss_val.item()
      if loss_val < best_val:
        best_val = loss_val
        best_model = copy.deepcopy(model)

  if viz_result == True:
    best_model.eval()
    y_train_pred = best_model(x_train[:-len(x_train)*val_size])
    y_train_pred = scaler.inverse_transform(y_train_pred.detach().numpy())
    y_val_pred = best_model(x_train[-len(x_train)*val_size:])
    y_val_pred = scaler.inverse_transform(y_val_pred.detach().numpy())
    y_pred = np.concatenate((y_train_pred, y_val_pred),axis = 0)
    print("true loss:",loss_fn(torch.Tensor(y_pred), torch.Tensor(ytrain)).item())

    # Visualising the results
    figure, axes = plt.subplots(figsize=(15, 6))
    axes.plot(y_train.detach().numpy(), color = 'blue', label = 'Real Stock Price')
    axes.plot(y_pred, color = 'red', label = 'Predicted Stock Price')
    #axes.xticks(np.arange(0,394,50))
    plt.axvline(len(y_tr)-len(x_train)*val_size, 0, 3500, label='validation line')
    plt.title('All Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
    
  return best_model

