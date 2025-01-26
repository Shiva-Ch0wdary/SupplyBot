from database import engine, SessionLocal
from models import Base, Supplier, Product

def init_db():
    Base.metadata.drop_all(bind=engine)  # Drop existing tables (for demo)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Create sample suppliers
    supplier1 = Supplier(
        name="Electro World",
        contact_info="contact@electroworld.com",
        product_categories_offered="laptops,phones"
    )
    supplier2 = Supplier(
        name="TechGear Supplies",
        contact_info="info@techgear.com",
        product_categories_offered="computers,accessories"
    )
    supplier3 = Supplier(
        name="Appliance Hub",
        contact_info="support@appliancehub.com",
        product_categories_offered="home appliances,kitchen gadgets"
    )
    supplier4 = Supplier(
        name="SmartTech Distributors",
        contact_info="sales@smarttech.com",
        product_categories_offered="smartphones,tablets,wearables"
    )

    db.add_all([supplier1, supplier2, supplier3, supplier4])
    db.commit()

    # Create sample products
    product1 = Product(
        name="Super Laptop 2000",
        brand="Brand A",
        price=1200.50,
        category="laptop",
        description="A high-performance laptop for gaming and work.",
        supplier_id=supplier1.id
    )
    product2 = Product(
        name="UltraPhone X",
        brand="Brand B",
        price=999.99,
        category="phone",
        description="A smartphone with advanced camera features.",
        supplier_id=supplier1.id
    )
    product3 = Product(
        name="Power Desktop",
        brand="Brand A",
        price=1500.00,
        category="desktop",
        description="A powerful desktop for professionals.",
        supplier_id=supplier2.id
    )
    product4 = Product(
        name="Smart Refrigerator 5000",
        brand="CoolTech",
        price=2000.00,
        category="home appliance",
        description="A smart refrigerator with Wi-Fi connectivity and advanced cooling features.",
        supplier_id=supplier3.id
    )
    product5 = Product(
        name="Turbo Blender Pro",
        brand="KitchenMasters",
        price=150.00,
        category="kitchen gadget",
        description="A high-speed blender for smoothies, soups, and more.",
        supplier_id=supplier3.id
    )
    product6 = Product(
        name="WearTech Smartwatch X2",
        brand="WearTech",
        price=250.00,
        category="wearable",
        description="A smartwatch with fitness tracking and voice assistant support.",
        supplier_id=supplier4.id
    )
    product7 = Product(
        name="Galaxy Tab Ultra",
        brand="Brand C",
        price=899.99,
        category="tablet",
        description="A powerful tablet for productivity and entertainment.",
        supplier_id=supplier4.id
    )
    product8 = Product(
        name="UltraHD 4K TV",
        brand="VisionPro",
        price=1200.00,
        category="home entertainment",
        description="A 65-inch 4K UltraHD TV with stunning visuals and built-in streaming apps.",
        supplier_id=supplier3.id
    )
    product9 = Product(
        name="Pro Gaming Chair",
        brand="GamerGear",
        price=299.99,
        category="accessory",
        description="An ergonomic gaming chair with adjustable lumbar support and RGB lighting.",
        supplier_id=supplier2.id
    )
    product10 = Product(
        name="Wireless Earbuds Plus",
        brand="AudioMax",
        price=149.99,
        category="audio",
        description="Noise-canceling wireless earbuds with immersive sound quality.",
        supplier_id=supplier4.id
    )
        # Additional Products
    product11 = Product(
        name="Noise-Canceling Headphones",
        brand="SoundPro",
        price=299.99,
        category="audio",
        description="Premium over-ear headphones with active noise cancellation and long battery life.",
        supplier_id=supplier4.id
    )
    product12 = Product(
        name="Gaming Keyboard X10",
        brand="GamerGear",
        price=129.99,
        category="accessory",
        description="Mechanical gaming keyboard with customizable RGB lighting.",
        supplier_id=supplier2.id
    )
    product13 = Product(
        name="Smart Thermostat 3.0",
        brand="HomeSmart",
        price=199.99,
        category="home automation",
        description="A Wi-Fi-enabled thermostat with energy-saving features.",
        supplier_id=supplier3.id
    )
    product14 = Product(
        name="Drone Pro Max",
        brand="SkyTech",
        price=999.99,
        category="drone",
        description="A professional-grade drone with 4K camera and GPS stabilization.",
        supplier_id=supplier4.id
    )
    product15 = Product(
        name="Portable Air Conditioner",
        brand="CoolMaster",
        price=450.00,
        category="home appliance",
        description="Energy-efficient portable air conditioner with remote control.",
        supplier_id=supplier3.id
    )
    product16 = Product(
        name="Advanced Fitness Tracker",
        brand="WearFit",
        price=129.99,
        category="wearable",
        description="A slim fitness tracker with heart rate monitoring and sleep tracking.",
        supplier_id=supplier4.id
    )
    product17 = Product(
        name="3D Printer MakerPro",
        brand="PrintTech",
        price=800.00,
        category="3d printer",
        description="A high-precision 3D printer for professionals and hobbyists.",
        supplier_id=supplier2.id
    )
    product18 = Product(
        name="Smart Doorbell Pro",
        brand="HomeSecure",
        price=249.99,
        category="home security",
        description="A smart doorbell with HD video, motion detection, and two-way audio.",
        supplier_id=supplier3.id
    )
    product19 = Product(
        name="Wireless Charging Pad",
        brand="PowerMax",
        price=49.99,
        category="accessory",
        description="A sleek wireless charging pad for Qi-compatible devices.",
        supplier_id=supplier4.id
    )
    product20 = Product(
        name="Electric Kettle Pro",
        brand="KitchenTech",
        price=79.99,
        category="kitchen gadget",
        description="A stainless steel electric kettle with temperature control.",
        supplier_id=supplier3.id
    )
    product21 = Product(
        name="Ergonomic Office Chair",
        brand="OfficeComfort",
        price=350.00,
        category="furniture",
        description="An ergonomic office chair with adjustable lumbar support.",
        supplier_id=supplier2.id
    )
    product22 = Product(
        name="Smart Washing Machine",
        brand="LaundryPro",
        price=1200.00,
        category="home appliance",
        description="A smart washing machine with app control and energy-saving mode.",
        supplier_id=supplier3.id
    )
    product23 = Product(
        name="Professional Camera X200",
        brand="PhotoMaster",
        price=1500.00,
        category="camera",
        description="A professional DSLR camera with 24MP sensor and 4K video recording.",
        supplier_id=supplier4.id
    )
    product24 = Product(
        name="Bluetooth Speaker Mini",
        brand="AudioMax",
        price=89.99,
        category="audio",
        description="A portable Bluetooth speaker with rich sound and long battery life.",
        supplier_id=supplier4.id
    )
    product25 = Product(
        name="Smart Light Bulb",
        brand="HomeBright",
        price=39.99,
        category="home automation",
        description="A color-changing smart bulb compatible with voice assistants.",
        supplier_id=supplier3.id
    )
    product26 = Product(
        name="Noise-Isolation Earbuds",
        brand="SoundPure",
        price=79.99,
        category="audio",
        description="Affordable earbuds with noise isolation and rich bass.",
        supplier_id=supplier4.id
    )
    product27 = Product(
        name="Smart Vacuum Cleaner",
        brand="CleanBot",
        price=499.99,
        category="home appliance",
        description="A robot vacuum cleaner with app control and multi-surface cleaning.",
        supplier_id=supplier3.id
    )
    product28 = Product(
        name="High-Speed USB Drive",
        brand="DataSaver",
        price=39.99,
        category="accessory",
        description="A 128GB USB drive with ultra-fast read and write speeds.",
        supplier_id=supplier2.id
    )
    product29 = Product(
        name="Laptop Cooling Pad",
        brand="TechCooling",
        price=49.99,
        category="accessory",
        description="A laptop cooling pad with adjustable fan speeds.",
        supplier_id=supplier1.id
    )
    product30 = Product(
        name="Gaming Mouse Elite",
        brand="GamerGear",
        price=89.99,
        category="accessory",
        description="A gaming mouse with customizable buttons and DPI settings.",
        supplier_id=supplier2.id
    )
    product31 = Product(
        name="Luxury Coffee Maker",
        brand="BrewMaster",
        price=249.99,
        category="kitchen gadget",
        description="A coffee maker with built-in grinder and programmable settings.",
        supplier_id=supplier3.id
    )
    product32 = Product(
        name="Electric Scooter Pro",
        brand="RideEasy",
        price=799.99,
        category="transport",
        description="An electric scooter with long battery life and fast charging.",
        supplier_id=supplier4.id
    )
    product33 = Product(
        name="Noise-Canceling Mic",
        brand="AudioPro",
        price=99.99,
        category="audio",
        description="A noise-canceling microphone for professional recordings.",
        supplier_id=supplier4.id
    )
    product34 = Product(
        name="VR Headset Elite",
        brand="VRWorld",
        price=599.99,
        category="vr device",
        description="A virtual reality headset with stunning visuals and motion tracking.",
        supplier_id=supplier4.id
    )
    product35 = Product(
        name="Smart Toaster",
        brand="KitchenMasters",
        price=149.99,
        category="kitchen gadget",
        description="A smart toaster with app control and customizable browning levels.",
        supplier_id=supplier3.id
    )
    product36 = Product(
        name="External Hard Drive 1TB",
        brand="DataSafe",
        price=89.99,
        category="storage",
        description="A 1TB external hard drive with fast transfer speeds.",
        supplier_id=supplier2.id
    )
    product37 = Product(
        name="Portable Projector",
        brand="VisionPro",
        price=699.99,
        category="home entertainment",
        description="A portable projector with Full HD resolution and HDMI input.",
        supplier_id=supplier3.id
    )
    product38 = Product(
        name="Compact Dishwasher",
        brand="CleanTech",
        price=799.99,
        category="home appliance",
        description="A compact dishwasher with energy-efficient cleaning cycles.",
        supplier_id=supplier3.id
    )
    product39 = Product(
        name="Advanced Weather Station",
        brand="WeatherPro",
        price=149.99,
        category="weather",
        description="A smart weather station with accurate temperature and humidity tracking.",
        supplier_id=supplier4.id
    )
    product40 = Product(
        name="High-End VR Treadmill",
        brand="VRMove",
        price=3000.00,
        category="vr device",
        description="A VR treadmill for immersive gaming and fitness applications.",
        supplier_id=supplier4.id
    )

    # Add the new products to the database
    db.add_all([
        product11, product12, product13, product14, product15, product16, product17, product18,
        product19, product20, product21, product22, product23, product24, product25, product26,
        product27, product28, product29, product30, product31, product32, product33, product34,
        product35, product36, product37, product38, product39, product40
    ])
    db.commit()


    db.add_all([
        product1, product2, product3, product4, product5,
        product6, product7, product8, product9, product10
    ])
    db.commit()

    db.close()
    print("Database initialized with updated sample data!")

if __name__ == "__main__":
    init_db()
