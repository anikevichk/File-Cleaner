#!/bin/bash
set -e

BASE="expected_final_data"

rm -rf "$BASE"

# Final cleaned X structure
mkdir -p "$BASE/X/cats/british"
mkdir -p "$BASE/X/cats/maine_coon"
mkdir -p "$BASE/X/dogs/labrador"
mkdir -p "$BASE/X/dogs/corgi"
mkdir -p "$BASE/X/rabbits/lop"
mkdir -p "$BASE/X/rabbits/angora"
mkdir -p "$BASE/X/hamsters/syrian"
mkdir -p "$BASE/X/hamsters/dwarf"



# Root file
echo "General pet archive: cats, dogs, rabbits and hamsters." > "$BASE/X/pets_index.txt"
echo "Backup file with mixed pet information." > "$BASE/X/backup_info.txt"

# Cats
echo "Cats like warm places and quiet corners." > "$BASE/X/cats/cats_general.txt"

echo "British cats are calm and friendly." > "$BASE/X/cats/british/british_info.txt"
echo "British cats have dense fur and round faces." > "$BASE/X/cats/british/british_notes.txt"

echo "New Maine Coon description: large, friendly cats with long fur." > "$BASE/X/cats/maine_coon/maine_coon_info.txt"
echo "New cat vaccination info: cats need basic vaccines and regular vet checks." > "$BASE/X/cats/cat_vaccination.txt"

# Dogs
echo "Dogs need walks, training, attention and regular vet checks." > "$BASE/X/dogs/dogs_general.txt"

echo "Labradors are friendly dogs." > "$BASE/X/dogs/labrador/labrador_info.txt"
echo "Cute labrador photo content." > "$BASE/X/dogs/labrador/labrador_photo.jpg"
echo "Labrador health information." > "$BASE/X/dogs/labrador/labrador_health.txt"

echo "Corgis have short legs and strong character." > "$BASE/X/dogs/corgi/corgi_info.txt"
echo "Corgi training notes." > "$BASE/X/dogs/corgi/corgi_training.txt"
echo "Corgi file with incorrect permissions." > "$BASE/X/dogs/corgi/corgi_permissions.txt"

# Rabbits
echo "Rabbits need hay, water and enough space." > "$BASE/X/rabbits/rabbits_general.txt"

echo "Lop rabbits have floppy ears." > "$BASE/X/rabbits/lop/lop_info.txt"

echo "Angora rabbits have long soft fur." > "$BASE/X/rabbits/angora/angora_info.txt"
echo "Angora rabbits need regular brushing." > "$BASE/X/rabbits/angora/angora_care.txt"
echo "Extra angora rabbit information missing in X." > "$BASE/X/rabbits/angora/angora_extra.txt"
echo "Rabbit file with problematic name." > "$BASE/X/rabbits/angora/rabbit_care_file_1.txt"

# Hamsters
echo "Hamsters sleep during the day and are active at night." > "$BASE/X/hamsters/hamsters_general.txt"

echo "New hamster care version: Syrian hamsters need food, water, a wheel and clean bedding." > "$BASE/X/hamsters/syrian/hamster_care.txt"
echo "Syrian hamsters usually live alone." > "$BASE/X/hamsters/syrian/syrian_notes.txt"

echo "Dwarf hamsters are small and fast." > "$BASE/X/hamsters/dwarf/dwarf_info.txt"
echo "Dwarf hamsters are active at night." > "$BASE/X/hamsters/dwarf/dwarf_hamster_facts.txt"

# Config file
cat > "$BASE/.clean_files" << 'EOF'
permissions=rw-r--r--
bad_chars=:";*?$#`|\
replacement=_
temp_extensions=.tmp,~
EOF

# Normalize permissions
find "$BASE" -type f -exec chmod 644 {} \;

echo "Expected final data created in: $BASE"
echo
echo "Expected final structure:"
find "$BASE" -print | sort