#!/bin/bash
# Ceremony: Encrypt ECM, burn public key, destroy private key

CORE_ID=$1
BUILD_DIR="build/ecm-${CORE_ID}"

echo "=== Building ECM Instance ${CORE_ID} ==="

# 1. Generate keys
echo "Generating ChaCha20-Poly1305 key..."
openssl rand -out ${BUILD_DIR}/ecm.key 32

echo "Generating Ed25519 keypair..."
ssh-keygen -t ed25519 -f ${BUILD_DIR}/ecm_keypair -N "" -C "ecm-${CORE_ID}"

# 2. Encrypt ECM software
echo "Encrypting ECM binary..."
chacha20poly1305_encrypt \
  --key ${BUILD_DIR}/ecm.key \
  --input cores/ecm-instances/ecm_software.bin \
  --output ${BUILD_DIR}/ecm_encrypted.bin

# 3. Burn public key to firmware
echo "Burning public key to firmware ROM..."
firmware_burn \
  --target 0xFF0000 \
  --source ${BUILD_DIR}/ecm_keypair.pub \
  --verify

# 4. Burn public key hash to fuse
echo "Burning public key hash to hardware fuse..."
hash=$(sha256sum ${BUILD_DIR}/ecm_keypair.pub | cut -d' ' -f1)
fuse_burn --address 0x0FE000 --data ${hash}

# 5. IRREVERSIBLE: Destroy private key
echo "SECURE ERASING PRIVATE KEY..."
shred -vfz -n 10 ${BUILD_DIR}/ecm.key
shred -vfz -n 10 ${BUILD_DIR}/ecm_keypair

echo "Verifying key absence..."
if [ -s ${BUILD_DIR}/ecm.key ]; then
    echo "ERROR: Key still exists!"
    exit 1
fi

echo "=== ECM ${CORE_ID} Built & Sealed ==="
echo "Public key: 0xFF0000 (firmware)"
echo "Public hash: 0x0FE000 (fuse)"
echo "Private key: DESTROYED"
echo "ECM state: OPAQUE & UNMODIFIABLE"