"""Dimension loading logic."""


def generate_surrogate_key(existing_count):
    """Generate warehouse surrogate key."""
    return existing_count + 1


def load_dimension(records, dimension_name):
    print(f"Loading {dimension_name} dimension: {len(records)} records")


if __name__ == "__main__":
    print("Dimension loader ready")
