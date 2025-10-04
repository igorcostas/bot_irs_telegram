#!/usr/bin/env python3
"""
Portfolio Image Generator for Freelancer.com
Creates a professional portfolio image showcasing the Marinete IRS Bot project
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap


def create_portfolio_image():
    """Generate a professional portfolio image"""

    # Image dimensions
    width = 1200
    height = 630  # Optimal for social media and portfolio sites

    # Colors
    bg_color = "#1a1a2e"  # Dark blue
    accent_color = "#16213e"  # Slightly lighter blue
    primary_text = "#ffffff"  # White
    secondary_text = "#e94560"  # Pink/Red accent
    tech_bg = "#0f3460"  # Medium blue

    # Create image
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use better fonts, fall back to default if not available
    try:
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
        )
        subtitle_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32
        )
        text_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20
        )
        small_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16
        )
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw background accent box
    draw.rectangle([(0, 0), (width, 120)], fill=accent_color)

    # Title
    title = "MARINETE"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(
        ((width - title_width) // 2, 25), title, fill=secondary_text, font=title_font
    )

    # Subtitle
    subtitle = "Portuguese IRS Tax Assistant Bot"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=text_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(
        ((width - subtitle_width) // 2, 85), subtitle, fill=primary_text, font=text_font
    )

    # Project Description
    y_position = 160

    # Section: About
    draw.text(
        (50, y_position),
        "AI-POWERED TELEGRAM BOT",
        fill=secondary_text,
        font=subtitle_font,
    )
    y_position += 50

    description = [
        "• Conversational AI assistant for Portuguese taxpayers",
        "• Interactive IRS simulation with 20 questions",
        "• Quick tax calculation and deduction guidance",
        "• Natural language processing using Groq API",
        "• Production-ready with comprehensive testing",
    ]

    for line in description:
        draw.text((50, y_position), line, fill=primary_text, font=text_font)
        y_position += 35

    # Technology Stack
    y_position += 20
    draw.text((50, y_position), "TECH STACK", fill=secondary_text, font=subtitle_font)
    y_position += 50

    # Technology boxes
    technologies = [
        "Python 3.12",
        "Telegram Bot API",
        "Groq AI",
        "Moonshot Kimi K2",
        "Poetry",
        "Git/GitHub",
        "Async/Await",
        "Testing Suite",
    ]

    tech_x = 50
    tech_y = y_position
    max_per_row = 4

    for i, tech in enumerate(technologies):
        if i > 0 and i % max_per_row == 0:
            tech_y += 45
            tech_x = 50

        # Draw tech box
        tech_bbox = draw.textbbox((0, 0), tech, font=small_font)
        tech_width = tech_bbox[2] - tech_bbox[0] + 20

        draw.rectangle(
            [(tech_x, tech_y), (tech_x + tech_width, tech_y + 35)],
            fill=tech_bg,
            outline=secondary_text,
            width=2,
        )
        draw.text((tech_x + 10, tech_y + 8), tech, fill=primary_text, font=small_font)

        tech_x += tech_width + 15

    # Footer
    footer_y = height - 60
    draw.rectangle([(0, footer_y), (width, height)], fill=accent_color)

    footer_text = "Python Developer | Bot Specialist | AI Integration Expert"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=text_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(
        ((width - footer_width) // 2, footer_y + 20),
        footer_text,
        fill=primary_text,
        font=text_font,
    )

    # Save image
    img.save("portfolio_marinete.png", "PNG", quality=95)
    print("✓ Portfolio image created: portfolio_marinete.png")
    return img


def create_tech_showcase_image():
    """Generate a technology showcase image"""

    width = 1200
    height = 800

    # Colors
    bg_color = "#0d1117"
    card_bg = "#161b22"
    border_color = "#30363d"
    text_color = "#c9d1d9"
    accent_color = "#58a6ff"
    success_color = "#3fb950"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42
        )
        section_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28
        )
        text_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
        )
        code_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16
        )
    except:
        title_font = ImageFont.load_default()
        section_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    # Title
    draw.text((50, 40), "Project Architecture", fill=accent_color, font=title_font)

    # Card 1: Backend
    draw.rectangle([(50, 120), (570, 350)], fill=card_bg, outline=border_color, width=2)
    draw.text((70, 140), "Backend Stack", fill=accent_color, font=section_font)

    backend_items = [
        "✓ Python 3.12.x",
        "✓ python-telegram-bot 21.11.1",
        "✓ Groq API Integration",
        "✓ Async/Await Architecture",
        "✓ Poetry Dependency Management",
    ]

    y = 190
    for item in backend_items:
        draw.text((90, y), item, fill=text_color, font=text_font)
        y += 30

    # Card 2: Features
    draw.rectangle(
        [(630, 120), (1150, 350)], fill=card_bg, outline=border_color, width=2
    )
    draw.text((650, 140), "Key Features", fill=accent_color, font=section_font)

    features = [
        "✓ Natural Language Processing",
        "✓ Context-Aware Conversations",
        "✓ Tax Calculations & Simulations",
        "✓ Multi-Command Interface",
        "✓ Secure Environment Config",
    ]

    y = 190
    for item in features:
        draw.text((670, y), item, fill=text_color, font=text_font)
        y += 30

    # Card 3: Code Quality
    draw.rectangle([(50, 390), (570, 720)], fill=card_bg, outline=border_color, width=2)
    draw.text((70, 410), "Code Quality", fill=success_color, font=section_font)

    quality_items = [
        "Tests: 5/5 Passing",
        "Coverage: Comprehensive",
        "Documentation: Complete",
        "Security: Best Practices",
        "Status: Production Ready",
    ]

    y = 460
    for item in quality_items:
        draw.text((90, y), item, fill=text_color, font=text_font)
        y += 40

    # Card 4: Quick Stats
    draw.rectangle(
        [(630, 390), (1150, 720)], fill=card_bg, outline=border_color, width=2
    )
    draw.text((650, 410), "Project Metrics", fill=success_color, font=section_font)

    stats = [
        "Lines of Code: 2000+",
        "Modules: 10+",
        "Commands: 7",
        "AI Model: Kimi K2",
        "Target: Portuguese Market",
    ]

    y = 460
    for item in stats:
        draw.text((670, y), item, fill=text_color, font=text_font)
        y += 40

    # Footer
    draw.text(
        (50, height - 50),
        "GitHub: github.com/yourusername/irs_telegram_bot",
        fill=accent_color,
        font=text_font,
    )

    img.save("portfolio_technical.png", "PNG", quality=95)
    print("✓ Technical showcase image created: portfolio_technical.png")
    return img


def create_simple_banner():
    """Create a simple, clean banner"""

    width = 1200
    height = 630  # Meet minimum requirement of 640x480

    # Gradient-like effect with two blues
    img = Image.new("RGB", (width, height), "#1e3a8a")
    draw = ImageDraw.Draw(img)

    # Create gradient effect
    for i in range(height):
        color_value = int(30 + (i / height) * 30)
        draw.rectangle([(0, i), (width, i + 1)], fill=f"#{color_value:02x}3a8a")

    try:
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72
        )
        subtitle_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36
        )
        text_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26
        )
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Main title
    title = "MARINETE BOT"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 120), title, fill="#ffffff", font=title_font)

    # Subtitle
    subtitle = "AI-Powered Portuguese Tax Assistant"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(
        ((width - subtitle_width) // 2, 230),
        subtitle,
        fill="#e0e0e0",
        font=subtitle_font,
    )

    # Tech stack
    tech = "Python • Telegram Bot • Groq AI • Production Ready"
    tech_bbox = draw.textbbox((0, 0), tech, font=text_font)
    tech_width = tech_bbox[2] - tech_bbox[0]
    draw.text(((width - tech_width) // 2, 320), tech, fill="#a0a0a0", font=text_font)

    # Tag line
    tagline = "Helping Portuguese taxpayers navigate IRS with intelligent automation"
    tagline_bbox = draw.textbbox((0, 0), tagline, font=text_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    draw.text(
        ((width - tagline_width) // 2, 380), tagline, fill="#c0c0c0", font=text_font
    )

    # Features
    features = [
        "✓ Natural Language Processing",
        "✓ 20-Question Tax Simulation",
        "✓ Quick Calculations & Deductions",
        "✓ 5/5 Tests Passing",
    ]

    y = 460
    for feature in features:
        feat_bbox = draw.textbbox((0, 0), feature, font=text_font)
        feat_width = feat_bbox[2] - feat_bbox[0]
        draw.text(
            ((width - feat_width) // 2, y), feature, fill="#90c090", font=text_font
        )
        y += 40

    img.save("portfolio_banner.png", "PNG", quality=95)
    print("✓ Simple banner created: portfolio_banner.png (1200x630)")
    return img


if __name__ == "__main__":
    print("Generating portfolio images...")
    print()

    # Generate all three variants
    create_portfolio_image()
    create_tech_showcase_image()
    create_simple_banner()

    print()
    print("=" * 50)
    print("All images generated successfully!")
    print("=" * 50)
    print()
    print("Files created:")
    print("  1. portfolio_marinete.png - Main portfolio image")
    print("  2. portfolio_technical.png - Technical showcase")
    print("  3. portfolio_banner.png - Simple banner")
    print()
    print("You can now upload these to Freelancer.com!")
