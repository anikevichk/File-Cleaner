#!/bin/bash

BASE="test_data"

rm -rf "$BASE"

# Main folders
mkdir -p "$BASE/X/cats/british"
mkdir -p "$BASE/X/cats/maine_coon"
mkdir -p "$BASE/X/dogs/labrador"
mkdir -p "$BASE/X/dogs/corgi"
mkdir -p "$BASE/X/rabbits/lop"
mkdir -p "$BASE/X/rabbits/angora"
mkdir -p "$BASE/X/hamsters/syrian"
mkdir -p "$BASE/X/hamsters/dwarf"

mkdir -p "$BASE/Y1/cats/british"
mkdir -p "$BASE/Y1/cats/maine_coon"
mkdir -p "$BASE/Y1/dogs/labrador"
mkdir -p "$BASE/Y1/dogs/corgi"
mkdir -p "$BASE/Y1/rabbits/lop"
mkdir -p "$BASE/Y1/rabbits/angora"
mkdir -p "$BASE/Y1/hamsters/syrian"
mkdir -p "$BASE/Y1/hamsters/dwarf"

mkdir -p "$BASE/Y2/cats/british"
mkdir -p "$BASE/Y2/cats/maine_coon"
mkdir -p "$BASE/Y2/dogs/labrador"
mkdir -p "$BASE/Y2/dogs/corgi"
mkdir -p "$BASE/Y2/rabbits/lop"
mkdir -p "$BASE/Y2/rabbits/angora"
mkdir -p "$BASE/Y2/hamsters/syrian"
mkdir -p "$BASE/Y2/hamsters/dwarf"

# Files directly in root directories
echo "General pet archive: cats, dogs, rabbits and hamsters." > "$BASE/X/pets_index.txt"
touch -d "12 days ago" "$BASE/X/pets_index.txt"

echo "General pet archive: cats, dogs, rabbits and hamsters." > "$BASE/Y1/pets_index_backup.txt"
touch -d "3 days ago" "$BASE/Y1/pets_index_backup.txt"

echo "Backup file with mixed pet information." > "$BASE/Y2/backup_info.txt"

# Files directly in animal folders
echo "Cats like warm places and quiet corners." > "$BASE/X/cats/cats_general.txt"
echo "Dogs need walks, training and attention." > "$BASE/X/dogs/dogs_general.txt"
touch -d "15 days ago" "$BASE/X/dogs/dogs_general.txt"

echo "Rabbits need hay, water and enough space." > "$BASE/X/rabbits/rabbits_general.txt"
echo "Hamsters sleep during the day and are active at night." > "$BASE/X/hamsters/hamsters_general.txt"

echo "Cats like warm places and quiet corners." > "$BASE/Y1/cats/cats_general_copy.txt"
echo "Dogs need walks, training, attention and regular vet checks." > "$BASE/Y1/dogs/dogs_general.txt"
touch -d "1 day ago" "$BASE/Y1/dogs/dogs_general.txt"

echo "Rabbits need hay, water and enough space." > "$BASE/Y2/rabbits/rabbits_general_backup.txt"
echo "Hamsters sleep during the day and are active at night." > "$BASE/Y2/hamsters/hamsters_general_copy.txt"

# Cat breed files
echo "British cats are calm and friendly." > "$BASE/X/cats/british/british_info.txt"
touch -d "10 days ago" "$BASE/X/cats/british/british_info.txt"

echo "British cats are calm and friendly." > "$BASE/Y1/cats/british/british_copy.txt"
touch -d "2 days ago" "$BASE/Y1/cats/british/british_copy.txt"

echo "British cats are calm and friendly." > "$BASE/Y2/cats/maine_coon/another_british_copy.txt"
touch -d "1 day ago" "$BASE/Y2/cats/maine_coon/another_british_copy.txt"

echo "Old Maine Coon description: large cats with long fur." > "$BASE/X/cats/maine_coon/maine_coon_info.txt"
touch -d "20 days ago" "$BASE/X/cats/maine_coon/maine_coon_info.txt"

echo "New Maine Coon description: large, friendly cats with long fur." > "$BASE/Y1/cats/maine_coon/maine_coon_info.txt"
touch -d "1 day ago" "$BASE/Y1/cats/maine_coon/maine_coon_info.txt"

echo "British cats have dense fur and round faces." > "$BASE/Y2/cats/british/british_notes.txt"

# Cat file placed in wrong folder in Y1, but it is newer
echo "Old cat vaccination info: cats need basic vaccines." > "$BASE/X/cats/cat_vaccination.txt"
touch -d "18 days ago" "$BASE/X/cats/cat_vaccination.txt"

echo "New cat vaccination info: cats need basic vaccines and regular vet checks." > "$BASE/Y1/dogs/cat_vaccination.txt"
touch -d "1 day ago" "$BASE/Y1/dogs/cat_vaccination.txt"

# Dog breed files
echo "Labradors are friendly dogs." > "$BASE/X/dogs/labrador/labrador_info.txt"
echo "Corgis have short legs and strong character." > "$BASE/X/dogs/corgi/corgi_info.txt"

echo "Cute labrador photo content." > "$BASE/X/dogs/labrador/labrador_photo.jpg"
touch -d "8 days ago" "$BASE/X/dogs/labrador/labrador_photo.jpg"

echo "Cute labrador photo content." > "$BASE/Y2/dogs/corgi/labrador_photo_copy.jpg"
touch -d "1 day ago" "$BASE/Y2/dogs/corgi/labrador_photo_copy.jpg"

echo "Temporary notes about labradors." > "$BASE/Y1/dogs/labrador/labrador_notes.tmp"
echo "Corgi training notes." > "$BASE/Y1/dogs/corgi/corgi_training.txt"

echo "Labrador health information." > "$BASE/Y2/dogs/labrador/labrador_health.txt"

# Empty file
touch "$BASE/X/dogs/corgi/empty_corgi_file.txt"

# File with bad permissions
echo "Corgi file with incorrect permissions." > "$BASE/Y2/dogs/corgi/corgi_permissions.txt"
chmod 777 "$BASE/Y2/dogs/corgi/corgi_permissions.txt"

# Rabbit breed files
echo "Lop rabbits have floppy ears." > "$BASE/X/rabbits/lop/lop_info.txt"
echo "Angora rabbits have long soft fur." > "$BASE/X/rabbits/angora/angora_info.txt"

echo "Lop rabbits have floppy ears." > "$BASE/Y1/rabbits/lop/lop_info_copy.txt"
echo "Angora rabbits need regular brushing." > "$BASE/Y1/rabbits/angora/angora_care.txt"

echo "Temporary backup about lop rabbits." > "$BASE/Y2/rabbits/lop/lop_backup~"
echo "Extra angora rabbit information missing in X." > "$BASE/Y2/rabbits/angora/angora_extra.txt"

# File with bad characters in name
echo "Rabbit file with problematic name." > "$BASE/X/rabbits/angora/rabbit:care?file#1.txt"

# Hamster breed files
echo "Old hamster care version: Syrian hamsters need food and water." > "$BASE/X/hamsters/syrian/hamster_care.txt"
touch -d "20 days ago" "$BASE/X/hamsters/syrian/hamster_care.txt"

echo "New hamster care version: Syrian hamsters need food, water, a wheel and clean bedding." > "$BASE/Y1/hamsters/syrian/hamster_care.txt"
touch -d "1 day ago" "$BASE/Y1/hamsters/syrian/hamster_care.txt"

echo "Dwarf hamsters are small and fast." > "$BASE/X/hamsters/dwarf/dwarf_info.txt"

echo "Dwarf hamsters are small and fast." > "$BASE/Y1/hamsters/dwarf/dwarf_info_copy.txt"
echo "Syrian hamsters usually live alone." > "$BASE/Y2/hamsters/syrian/syrian_notes.txt"
echo "Dwarf hamsters are active at night." > "$BASE/Y2/hamsters/dwarf/dwarf_hamster_facts.txt"

# Config file
cat > "$BASE/.clean_files" << 'EOF'
permissions=rw-r--r--
bad_chars=:";*?$#`|\
replacement=_
temp_extensions=.tmp,~
EOF

echo "Test data created in $BASE"
echo "Run your script like:"
echo "python3 clean_files.py --config test_data/.clean_files test_data/X test_data/Y1 test_data/Y2"