import random

# Visual Artists
artists = [
    "Van Gogh", "Picasso", "Monet", "Da Vinci", "Michelangelo", "Rembrandt",
    "Dali", "Warhol", "Pollock", "Matisse", "Cezanne", "Renoir", "Degas",
    "Hokusai", "Frida Kahlo", "Georgia O'Keeffe", "Basquiat", "Banksy",
    "Rothko", "Kandinsky", "Mondrian", "Magritte", "Escher", "Caravaggio",
    "Botticelli", "Raphael", "Toulouse-Lautrec", "Gauguin", "Manet",
    "Klimt", "Schiele", "Bacon", "Hockney", "Hopper", "Wyeth"
]

# Art Styles and Movements
art_styles = [
    "impressionist", "cubist", "surrealist", "abstract expressionist",
    "pop art", "art nouveau", "baroque", "renaissance", "romantic",
    "realist", "minimalist", "fauvism", "dadaism", "pointillism",
    "expressionist", "futurist", "constructivist", "art deco",
    "photorealistic", "hyperrealistic", "watercolor", "oil painting",
    "digital art", "concept art", "street art", "graffiti style",
    "comic book style", "anime style", "manga style", "ukiyo-e"
]

# Film Directors (for cinematic styles)
directors = [
    "Kubrick", "Hitchcock", "Scorsese", "Tarantino", "Spielberg",
    "Wes Anderson", "Tim Burton", "David Lynch", "Ridley Scott",
    "Christopher Nolan", "Akira Kurosawa", "Wong Kar-wai",
    "Terrence Malick", "Denis Villeneuve", "Coen Brothers",
    "Paul Thomas Anderson", "Darren Aronofsky", "Guillermo del Toro"
]

# Photography Styles
photo_styles = [
    "film noir", "golden hour", "blue hour", "high contrast",
    "black and white", "sepia", "vintage", "polaroid", "35mm film",
    "macro photography", "wide angle", "telephoto", "bokeh",
    "street photography", "portrait photography", "landscape photography"
]

# Digital/Modern Styles
digital_styles = [
    "cyberpunk", "steampunk", "vaporwave", "synthwave", "pixel art",
    "low poly", "isometric", "neon", "glitch art", "holographic",
    "matte painting", "concept art", "game art", "3D render"
]

def get_random_styles(count: int = 5) -> list[str]:
    # Combined list for easy random selection
    all_styles = artists + art_styles + directors + photo_styles + digital_styles
    random.shuffle(all_styles)
    return all_styles[:count]
