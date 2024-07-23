def get_area(side_len: float) -> float:
    pi = 3.14
    circle_area = pi * (side_len/4)**2 
    return circle_area

def get_plants(area: float, plant_spacing:float) -> int:
    plants = int(area / plant_spacing ** 2)
    return plants

def get_garden_plants(side_len: float, plant_spacing:float) -> None:
    circle_area = get_area(side_len)
    circle_plants = get_plants(circle_area, plant_spacing)
    semi_plants = get_plants(circle_area / 2, plant_spacing) 
    total_plants = circle_plants + semi_plants * 4
    print("Plants for each semicircle garden:", semi_plants)
    print("Plants for the circle garden:", circle_plants)
    print("Total plants for garden:", total_plants)

def get_garden_fill(side_len: float, fill_depth: float) -> None:
    fill_area = side_len**2 - get_area(side_len) * 3
    total_fill = fill_area/9 * fill_depth/3
    print("Total fill for the garden:", round(total_fill, 1), "cubic yards")

def get_garden_soil(side_len:float, soil_depth:float) -> None:
    circle_soil = get_area(side_len)/9 * soil_depth/3
    total_soil = circle_soil * 3
    print("Soil for each semicircle garden:", round(circle_soil/2, 1), "cubic yards")
    print("Soil for the circle garden:", round(circle_soil, 1), "cubic yards")
    print("Total soil for the garden:", round(total_soil, 1), "cubic yards")

def main() -> None:
    side_len = float(input("Enter length of side of garden (feet): "))
    plant_spacing = float(input("Enter spacing between plants (feet): "))
    soil_depth = float(input("Enter depth of garden soil (feet): "))
    fill_depth = float(input("Enter depth of fill (feet): "))
    print()
    get_garden_plants(side_len, plant_spacing)
    get_garden_soil(side_len,soil_depth)
    get_garden_fill(side_len, fill_depth)

main()
