from avatar_generator import AvatarGenerator


def generate_avatar():
    generator = AvatarGenerator("./photos")
    generator.generate_avatar(5)

    
if __name__ == "__main__":
    print(generate_avatar())
