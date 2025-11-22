# experiments/controller.py

import torch
import torch.nn as nn


# ----------------------------------------------------
# Ground Robot SAFE controller (2D → 2D)
# ----------------------------------------------------
class GroundRobotController(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 2)   # control = (ux, uy)
        )

        # small weights for stability / "safe" behavior
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.uniform_(m.weight, -0.05, 0.05)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        if not torch.is_tensor(x):
            x = torch.tensor(x, dtype=torch.float32)
        return self.net(x)


# Default instance for safe Ground Robot
ground_robot_controller = GroundRobotController()


# ----------------------------------------------------
# Ground Robot BUGGY controller (2D → 2D)
# – Same architecture, but pushes toward unsafe region
# ----------------------------------------------------
class BuggyGroundRobotController(GroundRobotController):
    def forward(self, x):
        out = super().forward(x)
        # BUG: add constant bias to drive robot toward unsafe box
        bias = torch.tensor([-1.0, 1.0], dtype=torch.float32)
        return out + bias


# ----------------------------------------------------
# Double Integrator SAFE controller (2D → 1D)
#   state = [pos, vel], control = [u]
# ----------------------------------------------------
class DoubleIntegratorController(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 1)   # scalar control
        )

        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.uniform_(m.weight, -0.05, 0.05)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        if not torch.is_tensor(x):
            x = torch.tensor(x, dtype=torch.float32)
        return self.net(x)


double_integrator_controller = DoubleIntegratorController()


# ----------------------------------------------------
# Quadrotor controller (6D → 3D)
#   state = [px, py, pz, vx, vy, vz]
#   control = [ax, ay, az]
# ----------------------------------------------------
class QuadrotorController(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 3)   # accelerations
        )

        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.uniform_(m.weight, -0.05, 0.05)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        if not torch.is_tensor(x):
            x = torch.tensor(x, dtype=torch.float32)
        return self.net(x)


quadrotor_controller = QuadrotorController()
