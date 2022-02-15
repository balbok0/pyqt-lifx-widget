import colorsys
import configparser

colors = {
    # https://coolors.co/eae4e9-fff1e6-fde2e4-fad2e1-e2ece9-bee1e6-f0efeb-dfe7fd-cddafd
    "magnolia": (234, 228, 233, 1),
    "linen": (255, 241, 230, 1),
    "misty-rose": (253, 226, 228, 1),
    "mimi-pink": (250, 210, 225, 1),
    "mint-cream": (226, 236, 233, 1),
    "powder-blue": (190, 225, 230, 1),
    "isabelline": (240, 239, 235, 1),
    "lavender-web": (223, 231, 253, 1),
    "periwinkle-crayola": (205, 218, 253, 1),

    # https://coolors.co/cb997e-ddbea9-ffe8d6-b7b7a4-a5a58d-6b705c
    "antique-brass": (203, 153, 126, 1),
    "desert-sand": (221, 190, 169, 1),
    "champagne-pink": (255, 232, 214, 1),
    "ash-gray": (183, 183, 164, 1),
    "artichoke": (165, 165, 141, 1),
    "ebony": (107, 112, 92, 1),
}

config = configparser.ConfigParser()
config['ColorPicker'] = {}
for idx, (_, c) in enumerate(colors.items()):
    config['ColorPicker'][f"{idx:02d}"] = "|".join(f"{x:.6f}" for x in colorsys.rgb_to_hsv(*c[:-1]))

with open("config/default-color-picker-custom-colors.ini", mode="w") as f:
    config.write(f)
