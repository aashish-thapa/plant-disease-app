# training script for the plant disease CNN
# run on google colab, use T4 GPU

import kagglehub
import os

path = kagglehub.dataset_download("abdallahalidev/plantvillage-dataset")
DATA_DIR = os.path.join(path, "plantvillage dataset", "color")
print("Found", len(os.listdir(DATA_DIR)), "classes")


# new cell
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms, models
import json, time
from tqdm import tqdm

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

full_dataset = datasets.ImageFolder(DATA_DIR, transform=train_transform)
class_names = full_dataset.classes
num_classes = len(class_names)

print(f"{len(full_dataset)} images, {num_classes} classes")

train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_set, val_set = random_split(full_dataset, [train_size, val_size])

val_set.dataset = datasets.ImageFolder(DATA_DIR, transform=val_transform)

train_loader = DataLoader(train_set, batch_size=128, shuffle=True, num_workers=2)
val_loader = DataLoader(val_set, batch_size=128, shuffle=False, num_workers=2)

print(f"Train: {train_size} | Val: {val_size}")


# new cell
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

# freeze everything except classifier
for param in model.features.parameters():
    param.requires_grad = False

model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(model.last_channel, num_classes)
)
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.classifier.parameters(), lr=0.001)


# new cell - training
EPOCHS = 5
best_acc = 0.0
history = {"train_loss": [], "val_loss": [], "val_acc": []}

for epoch in range(EPOCHS):
    t0 = time.time()

    model.train()
    running_loss = 0.0
    for imgs, lbls in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}"):
        imgs, lbls = imgs.to(device), lbls.to(device)
        optimizer.zero_grad()
        out = model(imgs)
        loss = criterion(out, lbls)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * imgs.size(0)

    train_loss = running_loss / train_size

    model.eval()
    vloss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for imgs, lbls in tqdm(val_loader, desc="Validating"):
            imgs, lbls = imgs.to(device), lbls.to(device)
            out = model(imgs)
            loss = criterion(out, lbls)
            vloss += loss.item() * imgs.size(0)
            _, preds = torch.max(out, 1)
            correct += (preds == lbls).sum().item()
            total += lbls.size(0)

    val_loss = vloss / val_size
    val_acc = correct / total

    history["train_loss"].append(train_loss)
    history["val_loss"].append(val_loss)
    history["val_acc"].append(val_acc)

    dt = time.time() - t0
    print(f"loss: {train_loss:.4f} - val_loss: {val_loss:.4f} - val_acc: {val_acc:.4f} - {dt:.0f}s")

    if val_acc > best_acc:
        best_acc = val_acc
        torch.save(model.state_dict(), "plant_disease_model.pth")
        print(f"  saved! ({val_acc:.4f})")

print(f"\nBest accuracy: {best_acc:.4f}")


# new cell
with open("class_names.json", "w") as f:
    json.dump(class_names, f, indent=2)

print(f"Saved {len(class_names)} class names")


# new cell - test
from PIL import Image
import random

model.load_state_dict(torch.load("plant_disease_model.pth", map_location=device))
model.eval()

print("Testing on 10 random images:")
for idx in random.sample(range(len(full_dataset)), 10):
    img_path, true_label = full_dataset.samples[idx]
    img = Image.open(img_path).convert("RGB")
    t = val_transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(t)
        probs = torch.nn.functional.softmax(out, dim=-1)[0]
        pred = probs.argmax().item()
        conf = probs[pred].item()

    ok = "ok" if pred == true_label else "WRONG"
    print(f"  [{ok}] actual: {class_names[true_label][:40]:40s} pred: {class_names[pred][:40]:40s} ({conf:.0%})")


# new cell
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(history["train_loss"], label="Train")
ax1.plot(history["val_loss"], label="Val")
ax1.set_title("Loss")
ax1.legend()
ax1.set_xlabel("Epoch")

ax2.plot(history["val_acc"])
ax2.set_title("Validation Accuracy")
ax2.set_xlabel("Epoch")
ax2.set_ylim(0.8, 1.0)

plt.tight_layout()
plt.savefig("training_curves.png", dpi=100)
plt.show()


# new cell - download
from google.colab import files
files.download("plant_disease_model.pth")
files.download("class_names.json")
files.download("training_curves.png")
