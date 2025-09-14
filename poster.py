from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random

# recolor some of the images to single color
def recolor_all_nontransparent(img, new_color=(0, 0, 0)):
    data = np.array(img)

    mask = data[:,:,3] > 0
    data[mask] = [new_color[0], new_color[1], new_color[2], 255]

    return Image.fromarray(data)


W, H = 1920, 1080
background = Image.new("RGB", (W, H), "#ffffffff")
bg_pixels = background.load()

top_color = (255, 105, 180)   
bottom_color = (255, 255, 255) 

# does the color gradient of the background
for y in range(H):
    r = int(top_color[0] + (bottom_color[0]-top_color[0]) * (y/H))
    g = int(top_color[1] + (bottom_color[1]-top_color[1]) * (y/H))
    b = int(top_color[2] + (bottom_color[2]-top_color[2]) * (y/H))
    for x in range(W):
        bg_pixels[x, y] = (r, g, b)

# for the horizontal binary texts on the bg
binary_background = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bi_bg_draw = ImageDraw.Draw(binary_background)

binary_font = ImageFont.truetype("arial.ttf", 16)
for i in range(0, W, 80):
    for j in range(0, H, 60):
        binary_str = ''.join(random.choice(['0', '1']) for _ in range(8))
        bi_bg_draw.text((i, j), binary_str, font=binary_font, fill=(255, 255, 255, 35))

background = Image.alpha_composite(background.convert("RGBA"), binary_background).convert("RGB")

# layering all the silhouettes and logos
chart_img = Image.open("chart.png").convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
background.paste(chart_img, None, mask = chart_img)

w_laptop = Image.open("w_laptop.png").convert("RGBA").resize((int(W/3), int(H/3)), Image.Resampling.LANCZOS)
w_laptop = recolor_all_nontransparent(w_laptop, new_color=(217, 165, 169))
background.paste(w_laptop, (0, H - w_laptop.size[1]), mask = w_laptop)

m_laptop = Image.open("m_laptop.png").convert("RGBA").resize((int(W/3), int(H/3)), Image.Resampling.LANCZOS)
m_laptop = recolor_all_nontransparent(m_laptop, new_color=(218, 165, 169))
background.paste(m_laptop, (W - m_laptop.size[0], H - m_laptop.size[1]), mask = m_laptop)

mascot = Image.open("mascot.png").convert("RGBA").resize((200,200), Image.Resampling.LANCZOS) 
background.paste(mascot, ((W - mascot.size[0]) - 30, 50), mask=mascot)

bisu = Image.open("logo.png").convert("RGBA").resize((200,200), Image.Resampling.LANCZOS)
background.paste(bisu, (50,50), mask=bisu)

silhouette = Image.open("sports_silhouette.png")
background.paste(silhouette, ((W - silhouette.size[0] - 50)//2, (H - silhouette.size[1])//2), mask=silhouette)


draw = ImageDraw.Draw(background)

slogan = ["Code Hard\nPlay Harder", "CCIS Phantoms"]

main_font = ImageFont.truetype("Orbitron-VariableFont_wght.ttf", 150) 
sub_font = ImageFont.truetype("Orbitron-VariableFont_wght.ttf", 40)

# creating bounding box and calculating x and y coordinates for the texts
bbox = draw.textbbox((0, 0), slogan[0], font=main_font)
main_text_w = bbox[2] - bbox[0]
main_text_h = bbox[3] - bbox[1]

sub_bbox = draw.textbbox((0, 0), slogan[1], font=sub_font)
sub_text_w = sub_bbox[2] - sub_bbox[0]
sub_text_h = sub_bbox[3] - sub_bbox[1]

x_main = (background.width - main_text_w) // 2
y_main = (background.height - (main_text_h + sub_text_h + 20)) // 2 

x_sub = (background.width - sub_text_w) // 2
y_sub = y_main + main_text_h + 30 

# draw.text((x_main+10, y_main+10), slogan[0], font=main_font, fill="#444444", align="center")
draw.text((x_main-10, y_main-10), slogan[0], font=main_font, fill="#444444", align="center")  
draw.text((x_main, y_main), slogan[0], font=main_font, fill="pink", align="center")

draw.text((x_sub-3, y_sub-3), slogan[1], font=sub_font, fill="#444444", align="center") 
draw.text((x_sub, y_sub), slogan[1], font=sub_font, fill="#ff1493", align="center")

background.show()
background.save("poster.png")


