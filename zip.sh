ZIP_NAME="hardware_security-NIKAS-IOANNIS-IASON_3771_TSOGKAS_TSIANTOS_DIMITRIOS_3796_PANAGIOTIS_3672.zip"

# Remove existing zip to avoid recursion
[ -f "$ZIP_NAME" ] && rm "$ZIP_NAME"

zip -r "$ZIP_NAME" .
