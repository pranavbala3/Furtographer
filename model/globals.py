import os

current_dir = os.path.dirname(os.path.abspath(__file__))
default_saved_model_name = '20231024-best_weights_resnet50.hdf5'
bottleneck_features_dir = os.path.join(current_dir, "bottleneck_features")
saved_models_dir = os.path.join(current_dir, "saved_models")
dataset_dir = os.path.join(current_dir, "datasets")
dog_data_dir = os.path.join(dataset_dir, "dogImages")
faces_data_dir = os.path.join(dataset_dir, "lfw")
train_set_dir = os.path.join(dog_data_dir, 'train')
valid_set_dir = os.path.join(dog_data_dir, 'valid')
test_set_dir = os.path.join(dog_data_dir, 'test')
dog_names = ['Affenpinscher', 'Afghan Hound', 'Airedale Terrier',
             'Akita', 'Husky', 'American Eskimo',
             'American Foxhound', 'American Staffordshire Terrier',
             'American Water Spaniel', 'Anatolian Shepherd',
             'Australian Cattle', 'Australian Shepherd',
             'Australian Terrier', 'Basenji', 'Basset Hound',
             'Beagle', 'Bearded Collie', 'Beauceron', 'Bedlington Terrier',
             'Belgian Malinois', 'Belgian Sheepdog', 'Belgian Tervuren',
             'Bernese Mountain', 'Bichon Frise',
             'Black And Tan Coonhound', 'Black Russian Terrier', 'Bloodhound',
             'Bluetick Coonhound', 'Border Collie', 'Border Terrier', 'Borzoi',
             'Boston Terrier', 'Bouvier Des Flandres', 'Boxer',
             'Boykin Spaniel', 'Briard', 'Brittany', 'Brussels Griffon',
             'Bull Terrier', 'Bulldog', 'Bullmastiff', 'Cairn Terrier',
             'Canaan', 'Cane Corso', 'Cardigan Welsh Corgi',
             'Cavalier King Charles Spaniel', 'Chesapeake Bay Retriever',
             'Chihuahua', 'Chinese Crested', 'Chinese Shar-Pei',
             'Chow Chow', 'Clumber Spaniel', 'Cocker Spaniel',
             'Collie', 'Curly-Coated Retriever',
             'Dachshund', 'Dalmatian', 'Dandie Dinmont Terrier',
             'Doberman Pinscher', 'Dogue De Bordeaux',
             'English Cocker Spaniel', 'English Setter',
             'English Springer Spaniel', 'English Toy Spaniel',
             'Entlebucher Mountain', 'Field Spaniel', 'Finnish Spitz',
             'Flat-Coated Retriever', 'French Bulldog', 'German Pinscher',
             'German Shepherd', 'German Shorthaired Pointer',
             'German Wirehaired Pointer', 'Giant Schnauzer',
             'Glen Of Imaal Terrier', 'Golden Retriever',
             'Gordon Setter', 'Great Dane', 'Great Pyrenees',
             'Greater Swiss Mountain', 'Greyhound', 'Havanese',
             'Ibizan Hound', 'Icelandic Sheepdog',
             'Irish Red And White Setter', 'Irish Setter', 'Irish Terrier',
             'Irish Water Spaniel', 'Irish Wolfhound', 'Italian Greyhound',
             'Japanese Chin', 'Keeshond', 'Kerry Blue Terrier', 'Komondor',
             'Kuvasz', 'Labrador Retriever', 'Lakeland Terrier',
             'Leonberger', 'Lhasa Apso', 'Lowchen', 'Maltese',
             'Manchester Terrier', 'Mastiff', 'Miniature Schnauzer',
             'Neapolitan Mastiff', 'Newfoundland', 'Norfolk Terrier',
             'Norwegian Buhund', 'Norwegian Elkhound', 'Norwegian Lundehund',
             'Norwich Terrier', 'Nova Scotia Duck Tolling Retriever',
             'Old English Sheepdog', 'Otterhound', 'Papillon',
             'Parson Russell Terrier', 'Pekingese',
             'Pembroke Welsh Corgi', 'Petit Basset Griffon Vendeen',
             'Pharaoh Hound', 'Plott', 'Pointer', 'Pomeranian', 'Poodle',
             'Portuguese Water', 'Saint Bernard', 'Silky Terrier',
             'Smooth Fox Terrier', 'Tibetan Mastiff',
             'Welsh Springer Spaniel', 'Wirehaired Pointing Griffon',
             'Xoloitzcuintli', 'Yorkshire Terrier']

num_dog_breeds = len(dog_names)
printing = 0
