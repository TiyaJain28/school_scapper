"""
Content Generator
Generates Kidrovia-format WordPress HTML content pages for each school.
Matches the exact structure of the provided sample template.
"""

from pathlib import Path
from src.scraper import SchoolRecord


def _safe(text: str, fallback: str = "") -> str:
    return text.strip() if text and text.strip() else fallback


def generate_page(school: SchoolRecord) -> str:
    """
    Generate WordPress block HTML for a school profile page.
    Matches the Columbia Grammar & Preparatory School sample template exactly.
    """
    name = _safe(school.name)
    city = _safe(school.city, "New York")
    website_url = school.website if school.website.startswith("http") else f"https://{school.website}"
    website_display = school.website.replace("https://", "").replace("http://", "").replace("www.", "")
    address = _safe(school.address, "New York, NY")
    phone = _safe(school.phone, "Contact via website")
    category = _safe(school.category, "Private Schools")

    # Enriched fields with sensible fallbacks
    founded = _safe(school.founded, "N/A")
    ages = _safe(school.ages, "K–12")
    students = _safe(school.students, "N/A")
    ratio = _safe(school.ratio, "N/A")
    school_type = _safe(school.school_type, category)
    annual_fee = _safe(school.annual_fee, "Contact school for current tuition information")
    tagline = _safe(school.tagline, f"Excellence in education at {name}.")
    about_long = _safe(
        school.about_long,
        school.description,
    )
    philosophy = _safe(
        school.philosophy,
        f"{name} delivers a rigorous, student-centered education focused on intellectual curiosity, "
        f"critical thinking, and character development. Faculty work closely with students to provide "
        f"personalized support while maintaining high academic standards.",
    )
    outcomes = _safe(
        school.outcomes,
        f"{name} prepares students for admission to highly selective colleges and universities. "
        f"The school's college-preparatory curriculum and individualized guidance help students "
        f"pursue ambitious academic and professional pathways.",
    )
    faculty = _safe(
        school.faculty,
        f"Experienced educators deliver rigorous academics while maintaining a personalized approach "
        f"to student development. Small class sizes allow meaningful mentorship and individualized attention.",
    )
    wellbeing = _safe(
        school.wellbeing,
        f"{name} prioritizes the academic, social, and emotional wellbeing of students through a "
        f"supportive environment that encourages confidence, belonging, and personal growth.",
    )
    curriculum = _safe(
        school.curriculum,
        f"The curriculum combines strong core academics with extensive opportunities in science, "
        f"mathematics, humanities, arts, and extracurricular activities. Programs are designed to "
        f"foster inquiry, creativity, and interdisciplinary thinking.",
    )
    achievements = _safe(
        school.achievements,
        f"{name} has a distinguished history and has produced notable alumni who have gone on to "
        f"leadership roles across academia, business, arts, and public service.",
    )
    facilities = _safe(
        school.facilities,
        f"Students benefit from extensive academic, athletic, arts, and recreational facilities. "
        f"Resources support classroom learning, research, athletics, and performing arts.",
    )
    admissions_info = _safe(
        school.admissions_info,
        f"{name} welcomes applications across all grade levels. The admission process includes "
        f"interviews, assessments, school records, and recommendations depending on grade level.",
    )
    deadline = _safe(school.application_deadline, "Contact school for application deadlines")
    image_url = _safe(
        school.image_url,
        "https://avenues.org/static/storyblok/112543/e89f4cbd93--900x846--dave-buckwald.jpg",
    )

    # Breadcrumb category slug
    cat_slug = category.lower().replace(" ", "-")
    city_slug = city.lower().replace(" ", "-")

    html = f"""<!-- wp:image {{"id":440,"sizeSlug":"full","linkDestination":"none"}} -->
<figure class="wp-block-image size-full"><img src="{image_url}" alt="{name}" class="wp-image-440"/></figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p><a href="elite-home.html">Elite</a> › <a href="elite-city-{city_slug}-new-york-us.html">{city}</a> › <a href="elite-program-{cat_slug}.html">{category}</a></p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Kidrovia Elite — Listed</h5>
<!-- /wp:heading --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{category}</h5>
<!-- /wp:heading --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"level":1}} -->
<h1 class="wp-block-heading"><em>{name}</em></h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{about_long}</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph -->
<p>{ages}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Ages</h5>
<!-- /wp:heading --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph -->
<p>{students}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Students</h5>
<!-- /wp:heading --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph -->
<p>{ratio}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Ratio</h5>
<!-- /wp:heading --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph -->
<p>{founded}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Founded</h5>
<!-- /wp:heading --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {{"width":"66.66%"}} -->
<div class="wp-block-column" style="flex-basis:66.66%"><!-- wp:heading -->
<h2 class="wp-block-heading">About <em>{name}</em></h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{about_long}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {{"width":"33.33%"}} -->
<div class="wp-block-column" style="flex-basis:33.33%"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Institution Details</h5>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Type</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Ages</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Students</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Ratio</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Founded</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">City</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Annual Fee</h5>
<!-- /wp:heading --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{school_type}</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{ages}</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{students}</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{ratio}</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{founded}</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{city}, New York, USA</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">{annual_fee}</h5>
<!-- /wp:heading --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Contact &amp; Enquiry</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading"><a href="{website_url}" target="_blank" rel="noreferrer noopener">{name} Official Website</a></h5>
<!-- /wp:heading --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"textAlign":"center","level":5}} -->
<h5 class="wp-block-heading has-text-align-center">Quote</h5>
<!-- /wp:heading -->

<!-- wp:paragraph {{"align":"center"}} -->
<p class="has-text-align-center">"{tagline}"</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"textAlign":"center","level":5}} -->
<h5 class="wp-block-heading has-text-align-center">— {name}</h5>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Philosophy</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How they <em>teach</em></h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{philosophy}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Outcomes</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Where students <em>go</em></h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{outcomes}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {{"level":4}} -->
<h4 class="wp-block-heading">Our Assessment</h4>
<!-- /wp:heading -->

<!-- wp:heading -->
<h2 class="wp-block-heading"><strong>How {name} Performs</strong></h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Expert Staff</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Faculty Excellence</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{faculty}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Student Care</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Student Wellbeing</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{wellbeing}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Curriculum</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Academic Integration</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{curriculum}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Achievements</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Competitive Pathway</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{achievements}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Facilities</h5>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Facilities &amp; Resources</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{facilities}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading -->
<h2 class="wp-block-heading">Admissions &amp;<br><em>How to Apply</em></h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{admissions_info}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Enquiries Open</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Applications Open for 2026–27 Academic Year</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Application Deadline</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{deadline}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Annual Fee</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{annual_fee}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Address</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{address}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Phone</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{phone}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Location</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{city}, New York, USA</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":5}} -->
<h5 class="wp-block-heading">Website</h5>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><a href="{website_url}" target="_blank" rel="noreferrer noopener">{website_display}</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:paragraph {{"align":"center"}} -->
<p class="has-text-align-center">"{tagline}"</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"textAlign":"center","level":5}} -->
<h5 class="wp-block-heading has-text-align-center">— {name}</h5>
<!-- /wp:heading -->
"""
    return html.strip()


def generate_all(schools: list, output_dir: str = "output/pages"):
    """Generate one HTML content file per school."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    generated = []

    for school in schools:
        slug = school.name.lower().replace(" ", "-").replace("&", "and").replace(",", "")
        filename = f"{output_dir}/{slug}.html"
        content = generate_page(school)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        generated.append({"name": school.name, "file": filename})
        print(f"Generated: {filename}")

    return generated
