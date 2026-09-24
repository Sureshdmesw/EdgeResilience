import torch
import torch.nn as nn

class TinyEdgeModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(17, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return torch.sigmoid(self.fc2(x))

model = TinyEdgeModel().eval()
x = torch.randn(1, 17)

torch.onnx.export(
    model,
    x,
    r".\models\edgeresilience\snapdragon\tiny_qnn_control.onnx",
    input_names=["features"],
    output_names=["score"],
    opset_version=17,
    dynamo=False,
)

print("created")
