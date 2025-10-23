from sentence_transformers import SentenceTransformer
import os
from PIL import Image
from glob import glob
import numpy as np
from rembg import remove

model = SentenceTransformer("clip-ViT-B-32")


def load_and_remove_bg(image_path):
    """Load image, resize if needed, and remove background."""
    input = Image.open(image_path).convert("RGB")  # Ensure 3 channels

    max_width = 1024
    if input.width > max_width:
        new_height = int(input.height * max_width / input.width)
        input = input.resize((max_width, new_height), Image.LANCZOS)

    no_bg_image = remove(input)
    return no_bg_image


def generate_clip_embeddings(images_path, model):

    image_extensions = ["jpg", "jpeg", "png", "webp"]

    # Get all image files with listed extensions
    image_paths = []
    for ext in image_extensions:
        pattern = os.path.join(images_path, f"**/*.{ext}")
        image_paths.extend(glob(pattern, recursive=True))

    embeddings = []
    for img_path in image_paths:
        image = Image.open(img_path)
        embedding = model.encode(image)
        embeddings.append(embedding)

    return embeddings, image_paths


IMAGES_PATH = "nail_dataset"

embeddings, image_paths = generate_clip_embeddings(IMAGES_PATH, model)

# def create_faiss_index(embeddings, image_paths, output_path):

#     dimension = len(embeddings[0])
#     index = faiss.IndexFlatIP(dimension)
#     index = faiss.IndexIDMap(index)

#     vectors = np.array(embeddings).astype(np.float32)

#     # Add vectors to the index with IDs
#     index.add_with_ids(vectors, np.array(range(len(embeddings))))

#     # Save the index
#     faiss.write_index(index, output_path)
#     print(f"Index created and saved to {output_path}")

#     # Save image paths
#     with open(output_path + '.paths', 'w') as f:
#         for img_path in image_paths:
#             f.write(img_path + '\n')

#     return index


# OUTPUT_INDEX_PATH = "/content/vector.index"
# index = create_faiss_index(embeddings, image_paths, OUTPUT_INDEX_PATH)

# def load_faiss_index(index_path):
#     index = faiss.read_index(index_path)
#     with open(index_path + '.paths', 'r') as f:
#         image_paths = [line.strip() for line in f]
#     print(f"Index loaded from {index_path}")
#     return index, image_paths

# index, image_paths = load_faiss_index(OUTPUT_INDEX_PATH)

# Convert to float32 numpy array
embedding_matrix = np.array(embeddings).astype(np.float32)

# Normalize embeddings (for cosine similarity)
embedding_matrix = embedding_matrix / np.linalg.norm(
    embedding_matrix, axis=1, keepdims=True
)

# Open your new image (replace with your actual image path)
query_image = "white oval shaped line"

# Get embedding
query_embedding = model.encode(query_image)

# Normalize it
query_embedding = query_embedding / np.linalg.norm(query_embedding)

# # Compute Euclidean distances
# distances = np.linalg.norm(embedding_matrix - query_embedding, axis=1)

# # Get indices of smallest distances
# top_indices = np.argsort(distances)[:5]

# Print closest matches
# for idx in top_indices:
#     print(f"Distance: {distances[idx]:.4f} — Image: {image_paths[idx]}")

# Compute dot product (cosine similarity)
similarities = np.dot(embedding_matrix, query_embedding)

# Get indices of top 5 most similar images
top_k = 5
top_indices = np.argsort(similarities)[::-1][:top_k]

# Print the most similar image paths
for idx in top_indices:
    print(f"Similarity: {similarities[idx]:.4f} — Image: {image_paths[idx]}")
