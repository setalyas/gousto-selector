# -*- coding: utf-8 -*-

from shiny import App, Inputs, Outputs, Session, reactive, ui
import random

### Recipe weights

recipe_weights = {
    "Cheesy Pecan & Squash Pasta Bake With Rocket": 909,
    "10-Min Lebanese Halloumi Wrap With Tahini Sauce": 377,
    "Cantonese-Style Soy-Baked Basa With Rice": 916,
    "Fable Mushroom 'Brisket' Sandwich With Pickles And Chunky Chips": 1266,
    "Chickpea, Spinach & Coconut Curry With Brown Rice": 1302,
    "Fiery Coconut Fish En Papillote With Rice": 398,
    "Extra Crispy Fish Goujons With Mixed Fries And Curry Ketchup": 1806,
    "Meat-Free Mince Wraps With Lime Mayo": 1728,
    "Vietnamese-Style Fable Mushroom & Lemongrass Stew": 1847,
    "10-Min Sicilian Haddock Stew & Lemony Couscous": 181,
    "Thai-Style Sweet Chilli Crispy Basa With Sticky Coconut Rice": 1798,
    "Baked Lemon & Herb Salmon With Cherry Tomatoes": 1637,
    "Herb-Crusted Salmon With Hasselback Potatoes ": 1707,
    "Big Flavour Beef Lasagne": 1875,
    "Extra Special Meat-Free Bangers 'N' Mash": 1518,
    "One-Pot Slow-Braised Mushroom Rogan Josh": 1399,
    "Lemony Smoked Fish & Spinach Linguine": 167,
    "Marmite Teriyaki Tofu & Sticky Rice": 419,
    "Spiced Paneer Nuggets, Chips & Masala Saag Beans": 1140,
    "Spelt, Feta & Roasted Grape Salad": 580,
    "Korean-Style Meat-Free Mince Bulgogi With Beans ": 1245,
    "Warm Harissa Chickpea & Giant Couscous Salad": 1854,
    "One-Pot Basa & Mexican-Style Rice With Lime Mayo": 1686,
    "Tantanmen Stir-Fried Tofu Ramen With Chilli Oil": 853,
    "Olive & Tomato Basa Stew With Crushed Potatoes And Olive Tapenade": 1427,
    "Coconutty Jerk-Spiced Basa Stew & Black Bean Rice": 1847,
    "Smoky Sweet Potato Salad & Guacamole Crostinis": 1420,
    "Georgian-Style Ajapsandali Stew With Herby Walnut Bulgur": 1637,
    "Seeded Goats' Cheese & Sweet Potato Salad": 246,
    "Feta Stuffed Squash With Herby Mixed Grains": 391,
    "Sweet 'N' Smoky BBQ Meat-Free Chick'n Fajitas": 1525,
    "Chipotle Meat-Free Burger With Caramelised Onions": 1420,
    "Sweet & Sour Crispy Tofu With Rice": 496,
    "Fragrant Coconut & Lemongrass Baked Pollock Curry": 965,
    "10-Min Smoked Fish & Spinach Pilau Rice": 265,
    "Tangy Lime Tofu With Sticky Ginger Rice": 1756,
    "Oven-Baked Mexican-Style Sweet Potato & Corn Broth": 1140,
    "Refried Bean & Corn Quesadillas": 1623,
    "Fruity Moroccan-Style Chickpea Stew With Couscous": 1168,
    "10-Min Creamy Haddock Encocado": 272,
    "10-Min Honey-Soy Salmon With Brown Rice & Pak Choi": 363,
    "Festive Double-Stacked Vegan Cheeseburger": 447,
    "Tex-Mex Loaded Sweet Potato Wedges": 489,
    "Smoky Fish Curry & Green Bean Rice": 28,
    "Oven-Baked Halloumi Ratatouille With Herby Rice": 1462,
    "All-In-One Spicy Meat-Free Mince Ragù Pasta": 1175,
    "Cheesy Veggie Burger With Chimichurri Mayo": 1637,
    "Leek & Roasted Tomato Mac 'N' Cheese": 251,
    "Indonesian Fiery Prawn Broth & Coconut Rice": 216,
    "Meat-Free Mince Thai-Style Larb": 1440,
    "Goats' Cheese, Spinach & Red Onion 'Squash-age' Roll": 1154,
    "Plant-Based Smashed Patty Burger Ft. Cheeze Fries": 1721,
    "Chipotle & Orange Oyster Mushroom Fajitas With Pineapple Salsa": 1385,
    "Coconut Peanut Curry with Crispy Fried Tofu": 1147,
    "Pistachio Pesto With Fresh Tagliatelle": 1364,
    "Korean-Style Tofu Jjigae Stew": 1294,
    "Veggie Fajita Pizza With Chipotle Mayo": 202,
    "Indian Lentil Salad & Sticky Paneer": 678,
    "Orzo Primavera With Tenderstem, Spinach & Green Beans": 300,
    "Oven-Baked Sticky Sesame Aubergine With Hoisin Rice ": 1659,
    "Crispy Tofu With Yellow Thai Curry And Rice": 1427,
    "Speedy Prawn & Pineapple Stir-Fry": 524,
    "Sticky Ginger Plant-Based Mince With Sesame Noodles": 1518,
    "Nutty Brazilian-Style Haddock Stew": 902,
    "Jamaican Squash & Coconut Stew": 190,
    "Smoky Fish Cakes, Greens & Curried Mayo": 489,
    "Veggie Philly Cheese'steak' With Loaded Cheesy Chips": 1588,
    "Butternut Squash & Cashew Saag With Pea & Mint Pilaf": 1399,
    "Meat-Free Mince Sticky Chilli Stir-Fry": 531,
    "10-Min Asian Meat-Free Mince Stir Fry": 223,
    "Creamy Harissa Basa Risotto With Crumbled Feta": 1469,
    "Butternut Squash & Sage Sauce With Spinach & Ricotta Ravioli ": 1385,
    "Lemon Butter Basa With Tomato & Spinach Pesto Rice": 1434,
    "Double Cheese Taco Rice With Chipotle Soured Cream": 1875,
    "Baked Harissa & Red Wine Orzo With Honey Greek Cheese": 1497,
    "10-Min Meat-Free Mince Bulgogi & Spicy Carrot Pickle": 363,
    "Moroccan-Style Squash Stew With Brown Rice": 1791,
    "Stroganoff Meat-Free Meatballs With Garlic Roast Potatoes": 1182,
    "South Indian-Style Paneer Cashew Curry": 1665,
    "Sticky Chilli Meat-Free Mince Burritos With Lime Mayo": 860,
    "Peruvian-Style Haddock & Sweet Potato Stew": 1091,
    "One-Pot Turkish-Style Fable Mushroom Bulgur Pilaf": 1483,
    "Smoky Meat-Free Mince Enchiladas With Tomato Salsa": 930,
    "One-Pot Smoky Spanish-Style Basa & Giant Couscous Stew": 1812,
    "Paneer Jalfrezi With Jeera Rice ": 1868,
    "Roasted Squash & Pecan Risotto With Crispy Sage": 43,
    "One-Pan Keralan-Style Basa Curry": 1616,
    "Indonesian-Style Basa Rendang With Green Bean Rice": 959,
    "Southern Thai-Style Haddock Panang Curry ": 842,
    "Roasted Tomato & Caramelised Onion Tart": 398,
    "10-Min Scrambled Tofu Fried Rice": 265,
    "Sticky Sesame Meat-Free Mince Stir-Fry": 1462,
    "Crispy Sumac Haddock & Vegetable Bulgur Lettuce Cups ": 1133,
    "Mediterranean-Style Vegetable Panzanella": 1623,
    "Creamy Sweet Potato & Sage Bonfire Night Pasty  ": 412,
    "Mexican-Style Meat-Free Meatballs & Tomato Rice": 1371,
    "10-Min Hoisin Pak Choi & Mushroom Stir Fry": 251,
    "Crispy Sumac Basa & Vegetable Bulgur Lettuce Cups": 1595,
    "Plant-Based Bacon Cheeseburger With Fancy Fries And Sweet Chilli Mayo": 902,
    "Spicy Coconut Basa Burger With Sunshine Mayo": 1791,
    "Oven-Baked Fable Mushroom 'Aloo Gosht'": 1806,
    "Sweet 'N' Smoky BBQ Chicken Fajitas": 1616,
    "Chickpea Tikka Masala With Fragrant Rice": 1182,
    "Chickpea And Tomato Sauce With Portobello Mushroom Tortelloni": 1140,
    "Teriyaki Basa With Sesame Greens": 1721,
    "Veg-Packed Minestrone Soup With Portobello Mushroom Tortelloni": 1238,
    "Spooky Squash, Spinach & Feta Pie": 412,
    "Seeded Fish, Lemonaise & British Asparagus ": 258,
    "Sweet Pepper & Tomato Sauce With Tomato & Mozzarella Tortelloni": 1798,
    "Thai-Style Butternut Squash Soup": 1161,
    "10-Min Spicy Halloumi Stew With Couscous": 146,
    "Smoky Bean Tacos With Chipotle Cream & Smashed Avocado": 1581,
    "Creamy Chickpea Curry Loaded Sweet Potato": 440,
    "One-Pot Ethiopian-Style Chicken Thigh & Sweet Potato Stew": 1440,
    "Chinese-Style Hot & Sour Prawn Stir-Fry ": 951,
    "Goats' Cheese & Portobello Mushroom Sandwich": 160,
    "Smoky Bean & Corn Empanadas With Herby Yoghurt": 1056,
    "Katsu Tofu With Sticky Rice And Salad": 842,
    "Vegan Burger With Figgy Onions & Herby Fries": 293,
    "Sticky Pomegranate Persian Halloumi": 524,
    "Chilli-Lime Sweet Potato Rice Salad": 216,
    "Steamed Miso Basa With Green Beans And Brown Rice": 1287,
    "Crunchy Tofu Satay & Noodle Salad": 1735,
    "Spicy Halloumi Stew With Sultana Couscous": 1623,
    "Loaded Patatas Rancheros With Greek Cheese": 1315,
    "All-In-One Meaty Pulled Mushroom & Gnocchi Cacio E Pepe": 1420,
    "Cheesy Muhammara Flatbread With Pomegranate Salad": 1707,
    "Lebanese-Spiced Rice & Crispy Fish": 601,
    "10-Min Indian Sticky Paneer & Lentil Salad": 279,
    "Baharat Meat-Free Mince Stew With Fruity Couscous": 1490,
    "Sticky Chilli Plant-Based Mince Stir-Fry": 1497,
    "Harissa Cod, Red Onion & Black Olive Bulgur": 300,
    "Oven-Baked Spiced Aubergine Tagine": 1056,
    "Chipotle Mushroom Burritos & Red Pepper Salsa": 258,
    "Meat-Free Sticky Chilli Stir Fry": 258,
    "Oven Baked Spicy Peri Peri Tofu Burger & Corn": 1532,
    "Chipotle Meat-Free Empanadas With Spicy Chimichurri Potatoes": 1448,
    "Heritage Tomato & Caramelised Onion Tart": 272,
    "Cheesy Tomato Gnocchi Tray Bake": 314,
    "Crispy Teriyaki Tofu With Sticky Rice & Sesame Edamame": 503,
    "Meat-Free Chicken Pad See Ew": 307,
    "10-Min Chicken Chow Mein": 188,
    "Plant-Based Burger With Figgy Onions And Herby Fries": 1413,
    "Golden Paneer Kati Rolls With Spicy Coriander Chutney": 1602,
    "Thai Crispy Fish With Tamarind Sauce": 440,
    "3-Mushroom Stroganoff With Herby Walnut Rice (DF)": 860,
    "Oven Baked Beef Goulash With Basmati Rice And Soured Cream": 1882,
    "Creamy Mushroom Stroganoff": 867,
    "Big Flavour Meat-Free Mince Lasagne ": 1602,
    "Coconutty Tamarind Aubergine & Green Bean Curry": 993,
    "Speedy Ginger & Chilli Prawns With Rice": 405,
    "Korean-Style Cheesy Corn With Gochujang Potatoes": 1434,
    "Pasta Alla Genovese": 377,
    "Roasted Sweet Potato With Jewelled Bulgur And Zhoug": 1721,
    "Aubergine Caponata Orzo With Crispy Capers": 1476,
    "Plant-Based Sweet Sesame Fable Mushroom Tacos": 1392,
    "Chermoula Couscous Stuffed Pepper": 1063,
    "Garlic Mushroom & Sage Gnocchi": 1728,
    "Meat-Free Chick'n & Pepper Chow Mein": 1323,
    "Fable Mushroom Teriyaki With Rice": 1882,
    "Mexican-Style Spiced Haddock Stew With Charred Corn Rice": 1378,
    "Thai-Style Coconut Udon Noodles With Crushed Peanuts": 1420,
    "Spicy Cajun-Style Basa & Pepper Stew": 1735,
    "Fragrant Lemongrass Prawn Stir-Fry With Black Rice ": 412,
    "10-Min Smoky Halloumi Tacos With Tomato Salsa": 426,
    "Meat-Free Sausages & Sweet Potato Mash": 139,
    "10-Min Smoky Spanish Garlic Prawns": 293,
    "Chickpea, Spinach & Coconut Curry With Rice": 909,
    "Moroccan-Style Chickpea & Sweet Potato Tagine": 1819,
    "Bats & Cobwebs Cheesy Squash Pasta Bake ": 1868,
    "Zingy Basa En Papillote With Vegetable Rice": 678,
    "Yasai Yaki Udon": 28,
    "The Ultimate Plant-Based Stack Burger": 1175,
    "Cheesy Beef Burger With Chimichurri Mayo": 1847,
    "The Henderson’s Relish Beef Burger": 1861,
    "Red Wine Fable Mushroom Ragù Tortiglioni With Garlic Pangrattato": 1371,
    "Sweet Chilli Fish & Sesame Pak Choi": 293,
    "Crispy Chilli Haddock With Pak Choi Noodles": 174,
    "Cheddar, Chilli & Mango Naan Toastie With Salad": 1728,
    "10-Min Spicy Veggie Noodles With Scrambled Tofu": 300,
    "Mushroom & Refried Bean Tacos With Zesty Apple Slaw": 678,
    "All-In-One Fragrant Coconutty Haddock Curry": 1440,
    "Marmite Teriyaki Tofu With Edamame Rice": 1882,
    "Halloumi Burger With Chimichurri Mayo & Wedges": 545,
    "Saag Aloo With Peas And Pitta": 1497,
    "Korean-Style Meat-Free Mince Bulgogi With Green Beans": 1833,
    "Smoky Meat-Free Mince, Pineapple & Red Onion Tacos": 1700,
    "Gambian-Style Fable Mushroom & Sweet Potato Peanut Stew": 1588,
    "Spiced Meat-Free Mince With Cucumber & Greek Cheese Bulgur": 1483,
    "Meat-Free Chick’n ‘Love Bun’ With TABASCO® Sauce": 1245,
    "Jerk-Spiced Basa With Coconut Brown Rice And Mango Salad": 1784,
    "Pizza Margherita With Chilli Oil": 363,
    "Basa Tom Kha Soup With Lemongrass Rice": 1819,
    "Creamy Garlic Mushroom Gnocchi": 1665,
    "Hoisin Tofu & Red Pepper Stir-Fry": 1833,
    "Asparagus & Goats' Cheese Risotto": 76,
    "Spicy Chipotle Steak, Black Bean Rice & Buttery Corn Cobette": 1826,
    "Fable Mushroom Tagine With Date Couscous": 1525,
    "Meat-Free Sausages With Honey-Mustard Salad": 190,
    "Leek & Triple Cheese Fondue With Fresh Tagliatelle": 1595,
    "10-Min Indian Paneer & Lentil Salad": 181,
    "Honey Mustard Meat-Free Sausage & Apple Salad": 580,
    "Fish Katsu With Amai Sauce & Ginger Slaw": 524,
    "Marmite Mushroom Carbonara": 426,
    "Leek & Mushroom Tart With Apple Walnut Salad": 279,
    "Roasted Squash, Jewelled Bulgur & Zhoug": 447,
    "Black Pepper Tofu Stir Fry With Rice": 1686,
    "Goats' Cheese, Leek & Spinach Pasta Bake": 1581,
    "Three-Cheese Corn Quesadillas With Tangy Chive Salad": 1406,
    "Peri-Peri Fable Mushroom x Chow Mein": 1098,
    "Mexican-Style Spiced Cod Stew With Charred Corn Rice": 1273,
    "Caribbean-Style Smoky Fish With Sweet Potato Mash": 440,
    "Simply Delicious King Prawn Stir-Fry": 1371,
    "Simply Perfect Beef Spag Bol": 1833,
    "Baja-Style Basa Tacos With Coriander Mayo": 1840,
    "Sicilian Pasta Alla Norma With Aubergine": 370,
    "Spicy Rice Noodle Soup With Sesame Korean-Style Tofu": 1392,
    "Plant-Based Black Bean & Sweet Potato Tortilla Pockets": 1427,
    "Keralan Jackfruit & Green Chilli Curry": 391,
    "Harissa Steak With Spiced Couscous & Feta Salad": 1854,
    "Smoky Pepper & Mushroom Pasta Bake": 1413,
    "Quick Shredded Hoisin Chicken Wraps ": 188,
    "Teriyaki Meat-Free Hot Dog Ft. Pineapple Salsa & Sriracha Mayo": 1798,
    "Brazilian-Style Black Beans With Zesty Lime Butternut Squash": 1735,
    "One-Pot North African-Style Chicken Tagine": 1448,
    "Three Cheese Melt With Homemade Onion & Grape Chutney": 377,
    "Hoisin Meat-Free Mince & Mushroom Rice Bowl": 1742,
    "Meat-Free Chicken Teriyaki Tray Bake": 405,
    "Mexican-Style Charred Corn & Chipotle Greek Cheese Salad": 1119,
    "Spiced Tofu Sofritas Bowl With Tomato Salsa": 1294,
    "Sesame Falafel Wraps With Sweet Chilli Mayo": 545,
    "Joe's Coconutty Thai Fish, Rice & Veg In A Bag": 209,
    "Big Flavour Meat-Free Mince Lasagne": 1525,
    "Baked Spicy Fable Mushroom Stew With Naan And Yoghurt ": 1427,
    "Crispy Smoky Tofu & Herby Rice Bowl": 1518,
    "10-Min Creamy Haddock Florentine Spaghetti": 62,
    "All-In-One Coconut & Lime Basa Chowder": 993,
    "Loaded Veggie Sweet Potato Nachos": 867,
    "Peri Peri Cheesy Butter Bean Burger With Chips & Sweetcorn": 1609,
    "Plant-Based Indonesian-Style Satay Noodles": 1679,
    "Plant-Based Sweet Chilli Tofu Stir Fry": 1784,
    "One-Pot Baked Mushroom Stroganoff Tortiglioni": 1504,
    "Sweet Pepper & Tomato Sauce With Fresh Tagliatelle ": 1806,
    "Spiced Butternut Squash & Pepper Stew": 1302,
    "10-Min Saag Aloo With Peas": 391,
    "Goan-Style Basa & Spinach Curry With Coriander Rice": 1302,
    "Speedy Harissa & Tomato Halloumi With Couscous ": 1287,
    "Carrot & Coriander Soup With Chutney Twists ": 594,
    "Indonesian-Style Meat-Free Mince & Green Bean Curry": 1036,
    "Smoked Fish Gratin, Spring Onion Mash & Garlicky Greens": 426,
    "All-In-One Mushroom Ragù Spaghetti With Caprese Salad": 1588,
    "10-Min Steamed Asian Fish With Brown Rice": 160,
    "One-Pot Smoky Spanish-Style Basa Stew & Giant Couscous": 1455,
    "Mexican-Style Basa Tray Bake With Lime Yoghurt": 1056,
    "Meat-Free Mince Kati Rolls With Coriander Chutney ": 1616,
    "Spicy Dan Dan-Style Tofu Udon": 1497,
    "Golden Paneer Kati Rolls With Coriander Chutney": 1455,
    "Giant Couscous Minestrone With Basil Oil": 1182,
    "Tofu Katsu With Sticky Rice And Salad": 1707,
    "Brazilian-Style Black Beans With Zesty Lime Basa": 1833,
    "Veggie Goulash, Potato Cakes & Sour Cream": 209,
    "Blackened Basa Tacos With Pineapple Salsa": 1756,
    "The Henderson’s Relish Meat-Free Burger": 1707,
    "Meat-Free Mince Tacos With Lime Mayo": 356,
    "Spinach & Caramelised Onion Tortilla Pizza": 62,
    "Keralan Squash Curry With Lime & Chilli Rice": 734,
    "Plant-Based Mushroom Pad See Ew-Style Noodles": 1462,
    "Meat-Free Tapas Burger With Bravas Relish And Aioli Wedges": 1889,
    "Vietnamese Scrambled Tofu & Noodle Broth": 160,
    "Zingy Fish En Papillote With Vegetable Rice": 307,
    "Tofu Pad Prik King With Lemongrass Rice": 1861,
    "King Prawn Paella With Aioli": 237,
    "Paneer Butter Masala With Rice And Naan": 1819,
    "Pizza Spinaci With Caramelised Onion": 489,
    "Simply Delicious Meat-Free Chick'n Stir-Fry": 1406,
    "Pistachio Pesto With Tomato & Mozzarella Tortelloni": 1742,
    "Leek & Potato Soup With Cheesy Marmite Toastie": 202,
    "Creamy Smoked Basa Potato-Topped Pie": 916,
    "The Ultimate Veggie Cheeseburger With Tomato Relish": 1434,
    "Harissa Halloumi Sandwich & Carrot Slaw": 246,
    "Creamy Chickpea Curry Loaded Baked Sweet Potato": 1154,
    "Spicy Veggie Noodles With Scrambled Tofu": 916,
    "Creamy Squash & Yellow Pepper Linguine With Zingy Pistachio Crumb": 1154,
    "Meat-Free Mince Thai Larb": 545,
    "Indonesian-Style Prawn Curry & Green Bean Rice": 132,
    "Lebanese-Style Halloumi Wrap With Tahini Sauce": 573,
    "Classic Chilli Con Carne": 1868,
    "Roasted Caprese Aubergine With Cheesy Pesto Beans": 1091,
    "Roasted Pepper & Goats' Cheese Tart": 405,
    "Mauritian Fish Vindaye With Buttery Bread": 223,
    "10-Min Fish Korma With Basmati Rice & Beans": 314,
    "Sichuan-Style Spicy Black Bean Tofu": 1518,
    "Portuguese-Style Basa Burritos With Spicy Rice & Peas": 1371,
    "10-Min Loaded Meat-Free Mince Chilli Nachos": 447,
    "Big Flavour Beef Lasagne ": 1889,
    "Georgian-Style Aubergine & Walnut Rolls": 1742,
    "Chettinad Chicken Curry": 188,
    "Meat-Free Mince & Black Bean Burrito Bowl": 1532,
    "Thai-Style Basa Burger With Crispy Fries & Sriracha Mayo": 1728,
    "Garlic & Coriander Butter Chickpea Burritos": 1462,
    "Harissa Meat-Free Meatballs With Roasted Pepper Couscous": 1756,
    "Chickpea Tikka Masala & Fragrant Rice": 251,
    "Tortilla-Topped Double Bean & Squash Chilli": 524,
    "Roasted Tomato Linguine With Pine Nut & Seed Pangrattato": 1686,
    "Joe’s Satay Sweet Potato & Kale Curry": 286,
    "Simply Perfect Meat-Free Mince Spag Bol": 1413,
    "One-Pot Cheesy Olive & Tomato Farfalle": 1525,
    "Harissa Chickpea & Apricot Tagine With Tahini Yoghurt": 1532,
    "Paneer & Mango Salad With Crispy Chickpeas": 531,
    "Sweetcorn & Pepper Masala Curry with Sultana Rice": 1392,
    "BBQ Mac & Cheese Meat-Free Hot Dog": 1812,
    "Crispy Tofu Pad Thai": 1840,
    "Oven-Baked Mexican Sweet Potato & Corn Broth": 1245,
    "10-Min Smoked Fish & Sweetcorn Wraps": 419,
    "Thai-Style Meat-Free Mince Rice With Mangetout": 1056,
    "Plant-Based Chipotle Squash & Bean Enchiladas": 1476,
    "Sweet Potato & Pepper Bulgur Salad": 1665,
    "10-Min Smoked Fish & Kale Pilau Rice": 356,
    "Herb-Crusted Basa With Romesco Potatoes And Aioli": 1014,
    "Plant-Based Creamy Leek & Mushroom Pie": 496,
    "Sweet Chilli Tofu With Veg-Packed Rice": 1385,
    "One-Pot Fable Mushroom Chilli With Salsa": 1715,
    "Sweet Chilli & Sesame Meat-Free Chicken Udon": 594,
    "Roasted Squash Grain Bowl, Miso-Tahini Dressing": 160,
    "Meat-Free Mince Meatballs With Herby Bulgur And Pepper Sauce": 1812,
    "Zanzibar-Style Haddock & Pepper Curry": 1259,
    "Mushroom & Broccoli Bowl With Miso Dressing": 153,
    "Veggie Udon Stir-Fry With Sesame Fried Egg": 734,
    "One-Pot Haddock Rogan Josh With Yoghurt": 1119,
    "Lebanese Spiced Rice & Crispy Fish": 76,
    "10-Min Chickpea, Spinach & Coconut Curry": 153,
    "Saucy Gochujang Chicken Breast Udon": 1469,
    "Spinach & Feta Tart, Crispy Potatoes & Salad": 237,
    "Mexican-Style Veggie Wraps With Crispy Onion Cobettes": 1504,
    "Smoky Pepper & Portobello Pasta Bake": 419,
    "Tamarind Sweet Potato & Coconut Rice with Salsa": 1483,
    "Baked Saffron, King Prawn & Pea Risotto With Lemon": 1469,
    "Caramelised Mushroom, Parsley & Walnut Speltotto": 1161,
    "Oven-Baked Slow-Braised Mushroom Rogan Josh": 1791,
    "Pizza Parmigiana With Aubergine": 356,
    "Warming Meat-Free Chick'n Bhuna With Rice And Naan": 1694,
    "Coconutty Curried Noodles With Crispy Tofu": 1868,
    "Nutty Three Veg Curry With Basmati Rice": 1182,
    "The Ultimate Veggie Cheeseburger & Tomato Relish": 314,
    "Spaghetti & Meat-Free Mince Meatballs": 153,
    "Creamy Cajun Mushroom & Pepper Linguine": 573,
    "Golden Harissa Basa En Croûte With Mint Yoghurt": 1413,
    "DIY Pizza Margherita With Chilli Oil": 496,
    "Paneer Butter Masala With Coriander Naan": 139,
    "Honey Soy Salmon With Brown Rice And Pak Choi": 1476,
    "Caribbean-Style Smoky Basa With Sweet Potato Mash": 1791,
    "Brazilian Haddock Moqueca & Zesty Lime Rice": 426,
    "Hungarian-Style Smoky Basa Soup With Sour Cream & Ciabatta": 1602,
    "Sicilian-Style Pasta Alla Norma With Aubergine": 1259,
    "Lentil & Sweetcorn Burger With Chipotle Mayo": 216,
    "Sticky Hoisin Tofu Burger & Red Cabbage Slaw": 531,
    "The Classic Plant-Based Cheezeburger With Sticky Onions": 1735,
    "Lemony Green Veg Gnocchi": 286,
    "Lebanese-Style Spiced Rice With Crispy Basa": 1715,
    "Paneer Pathia With Turmeric Rice And Naan": 1133,
    "Scott & Wilson's Squash & Garlic Mushroom Gnocchi": 601,
    "Smoky Meat-Free Chilli Con Carne With Rice": 1826,
    "Roasted Tomato Linguine With Basil & Seed Crumb": 265,
    "10-Min Cheesy Gochujang Udon Noodles With Ginger Salad ": 1259,
    "Ginger-Poached Fish In Udon Broth": 43,
    "10-Min Chilli Paneer Masala": 167,
    "Paneer Jalfrezi With Buttery Cardamom Rice & Naan": 363,
    "Jewelled Bulgur With Feta & Sumac Fried Egg": 503,
    "Smoky Basa Tacos With Zingy Corn & Black Bean Salsa": 1161,
    "Sweet & Sour Meat-Free Chick'n With Rice": 1679,
    "Crispy Basa With Vegetable Miso Broth": 1861,
    "Zingy Salmon With Lime & Chilli Noodles": 1875,
    "Easy One-Pot Haddock & Leek Risotto": 62,
    "Simply Delicious Meat-Free Chicken Stir-Fry": 1014,
    "Mexican Meat-free Meatballs & Tomato Rice": 1302,
    "Meat-Free Sausage & Pesto Sandwich": 174,
    "Lebanese-Style Halloumi Wraps With Tahini Sauce": 734,
    "One-Pot Chicken Breast Paella With Roasted Garlic Aioli": 1420,
    "Goats' Cheese & Roasted Mushroom Sandwich": 265,
    "The Ultimate Vegan Stack Burger": 300,
    "Crispy Baked Tacos, Refried Beans & Pineapple Salsa": 594,
    "Butternut Squash Bhuna & Cardamom Rice": 419,
    "Oven-Baked Fable Mushroom BBQ Beans": 1133,
    "Smoky Halloumi Tacos With Tomato Salsa": 580,
    "Curried Basa, Cherry Tomato & Spinach Noodle Soup": 1694,
    "The Classic Meat-Free Cheeseburger": 1378,
    "Peri-Peri Halloumi Burger With Fries & Peri-nnaise": 1715,
    "Sweet Potato & Spinach Curry With Saffron Rice": 237,
    "Spinach & Paneer Curry With Cardamom Rice": 307,
    "Feta & Sweet Potato Taquitos": 398,
    "Coconut Haddock Curry With Green Beans": 1889,
    "Baked Butternut Squash Biryani & Coconut Yoghurt": 545,
    "Crispy Teriyaki Tofu With Sticky Rice & Sesame Broccoli": 21,
    "Meat-Free Sausages With Sweet Potato Mash": 1014,
    "Winter Squash & Sweet Potato Gratin": 62,
    "Nutty Lemongrass & Haddock Stir Fry": 503,
    "Fable Mushroom & Cashew Massaman Curry With Rice": 1854,
    "Homemade Chicken Goujons & Cheesy Beans": 188,
    "Scrambled Tofu Yaki Udon With Rainbow Veg": 601,
    "Mexican Feast with Pulled Mushroom Birria Tacos": 965,
    "Cheesy Baked Veggie Enchiladas": 1511,
    "Cheesy Baked Basa And Pea Greens With Garlic Butter": 1798,
    "Herby Meat-Free Mince Gnocchi Bolognese": 1637,
    "Creamy Pesto & Pea Farfalle": 1875,
    "Veggie Goulash With Potato Cakes And Sour Cream": 965,
    "Palak Paneer With Cardamom Rice": 1889,
    "Manchurian-Style Chilli Paneer With Sesame Fried Rice": 1861,
    "Messy Aubergine & Spinach Lasagne": 1427,
    "Punjabi-Style Black Dal Makhani With Cumin Rice ": 237,
    "Nutty Brazilian Fish Stew": 580,
    "Goan-Style Basa & Spinach Curry With Parsley Rice": 1854,
    "Keralan-Style Squash Curry With Lime & Chilli Rice": 1826,
    "Butternut Squash & Goats' Cheese Tart": 202,
    "Salt & Pepper Prawns With Egg Fried Rice": 930,
    "Vietnamese-Style Fable Mushroom Rice Bowl": 1504,
    "Spiced Basa Wraps With Tomato Salad And Mint Chutney ": 1581,
    "One-Pot Plant-Based Tortiglioni Puttanesca": 1672,
    "10-Min Blackened Fish Tacos & Pineapple Salsa": 447,
    "Assassin's Spaghetti With Rocket & Olive Salad": 1469,
    "One-Pot Slow Braised Mushroom Rogan Josh": 930,
    "10-Min Meat-Free Mince Thai Larb": 412,
    "Baked Bengali-Style Mustard & Coconut Haddock Curry": 1490,
    "Asparagus & Flaked Almond Risotto": 314,
    "Chilli Paneer Masala With Brown Rice And Naan": 1882,
    "Chinese-Style Meat-Free Mince & Green Pepper Stir-Fry With Rice": 1490,
    "Korean Prawn Jjam-Pong Noodle Soup": 594,
    "Chinese-Style Tofu & Pepper Chow Mein": 1323,
    "Herby Smoked Basa & Leek Pie": 1609,
    "One Pot Turkish-Style Fable Mushroom Bulgur Pilaf": 1742,
    "10-Min Beany Avo Tacos": 21,
    "Mexican-Style Feast with Pulled Mushroom Birria Tacos": 1686,
    "Tangy Tomato Soup, Goats' Cheese & Basil Focaccia": 503,
    "Slow-Roasted Heritage Tomato, Feta & Lentil Salad": 258,
    "Squash & Lentil Balls With Creamy Tomato Linguine": 1084,
    "The Ultimate Christmas Vegan Burger": 76,
    "Garlicky Prawns With Green Butter Orzo": 391,
    "Baja-Style Fish Tacos With Coriander Mayo": 246,
    "Meat-Free Bangers & Beans With Cheesy Potato Skins": 1147,
    "Portobello Mushroom Rogan Josh": 181,
    "Lebanese-Spiced Rice With Crispy Basa": 734,
    "Oven-Baked Coconutty Vegetable Curry": 1238,
    "Baked Bengali-Style Mustard & Coconut Cod Curry": 1266,
    "Pan-Fried Fish With Gnocchi, Mushrooms & Spinach": 531,
    "Smoky Basa Tacos With Zingy Black Bean & Tomato Salsa": 1819
}

### Get the recipes

ui_app = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("n", "How many recipes?", 2, 10, 5),
        ui.input_text("keyword", "Keyword to filter by:")
    ),
    ui.input_action_button("add", "Draw some recipes"),
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.effect
    @reactive.event(input.add)
    def _():
        if len(input.keyword()) > 0:
            recipes = {k:v for k,v in recipe_weights.items() if input.keyword().lower() in k.lower()}
        else:
            recipes = recipe_weights.copy()
        recipe_list = random.choices(list(recipes.keys()),
                                 weights=list(recipes.values()),
                                 k=input.n())
        recipe_list_str = '\n'.join([f'- {a}' for a in recipe_list])
        ui.remove_ui(selector="p")
        ui.remove_ui(selector="ul")
        ui.insert_ui(
            ui.markdown(f"""This selection is:\n\n{recipe_list_str}"""),
            selector="#add",
            where='afterEnd'
        )

app = App(ui_app, server)