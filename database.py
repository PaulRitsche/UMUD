from deta import Deta

# Initialize Deta Base
DETA_PROJECT_KEY = "bLbnQSkX_JNprytFEx1rVKBSdWRZRj19qtmxXMgHs"
deta = Deta(DETA_PROJECT_KEY)
db = deta.Base("muscle_ultrasound_metadata")

print(db)
dp.put({"name": "test", "age": 25, "sex": "male"})

# Example data
example_data = [
    {
        "muscle": "Biceps",
        "image_type": "Type1",
        "device": "DeviceA",
        "age": 25,
        "sex": "Male",
        "height": 180,
        "weight": 75,
        "dataset_link": "https://example.com/dataset1",
    },
    {
        "muscle": "Triceps",
        "image_type": "Type2",
        "device": "DeviceB",
        "age": 30,
        "sex": "Female",
        "height": 165,
        "weight": 60,
        "dataset_link": "https://example.com/dataset2",
    },
    {
        "muscle": "Quadriceps",
        "image_type": "Type3",
        "device": "DeviceC",
        "age": 40,
        "sex": "Male",
        "height": 175,
        "weight": 80,
        "dataset_link": "https://example.com/dataset3",
    },
]


def insert_dataset(dataset):
    return db.put(dataset)


def fetch_all_datasets():
    res = db.fetch().items
    return res


def get_dataset(muscle, image_type, device, age, sex, height, weight):
    res = db.get(
        {
            "muscle": muscle,
            "image_type": image_type,
            "device": device,
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
        }
    )
    return res


insert_dataset(example_data[0])
print(fetch_all_datasets())
print(get_dataset("Biceps", "Type1", "DeviceA", 25, "Male", 180, 75))
