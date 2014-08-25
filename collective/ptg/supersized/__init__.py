from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema
try:
    import json
except ImportError:
    import simplejson as json

_ = MessageFactory('collective.ptg.supersized')

class ISupersizedDisplaySettings(IBaseSettings):
    supersized_slideshow = schema.Bool(
        title=_(u"label_slideshow",
            default=u"Slideshow on"),
        default=True)
    supersized_stop_loop = schema.Bool(
        title=_(u"label_stop_loop",
            default=u"Pauses slideshow on last slide"),
        default=False)
    supersized_transition = schema.Choice(
        title=_(u"label_supersized_transition",
            default=u"Transition"),
        default=1,
        vocabulary=SimpleVocabulary([
            SimpleTerm(0, 0,
                _(u"label_supersized_transition0", default=u"None")),
            SimpleTerm(1, 1,
                _(u"label_supersized_transition1", default=u"Fade")),
            SimpleTerm(2, 2,
                _(u"label_supersized_transition2", default=u"Slide Top")),
            SimpleTerm(3, 3,
                _(u"label_supersized_transition3", default=u"Slide Right")),
            SimpleTerm(4, 4,
                _(u"label_supersized_transition4", default=u"Slide Bottom")),
            SimpleTerm(5, 5,
                _(u"label_supersized_transition5", default=u"Slide Left")),
            SimpleTerm(6, 6,
                _(u"label_supersized_transition6", default=u"Carousel Right")),
            SimpleTerm(7, 7,
                _(u"label_supersized_transition7", default=u"Carousel Left")
            )
        ]))
    supersized_performance = schema.Choice(
        title=_(u"label_performance",
            default=u"Performance"),
        default=1,
        vocabulary=SimpleVocabulary([
            SimpleTerm(0, 0,
                _(u"label_supersized_performance0", default=u"Normal")),
            SimpleTerm(1, 1,
                _(u"label_supersized_performance1",
                    default=u"Hybrid between speed and quality")),
            SimpleTerm(2, 2,
                _(u"label_supersized_performance2",
                    default=u"Optimizes image quality")),
            SimpleTerm(3, 3,
                _(u"label_supersized_performance3",
                    default=u"Optimizes transition speed. Only works for "
                            u"Firefox, IE, not Webkit")
            )
        ]))
    supersized_min_width = schema.Int(
        title=_(u"label_min_width",
            default=u"Min width allowed, in pixels"),
        default=0)
    supersized_min_height = schema.Int(
        title=_(u"label_min_height",
            default=u"Min height allowed, in pixels"),
        default=0)
    supersized_horizontal_center = schema.Bool(
        title=_(u"label_horizontal_center",
            default=u"Horizontally center background"),
        default=True)
    supersized_vertical_center = schema.Bool(
        title=_(u"label_vertical_center",
            default=u"Vertically center background"),
        default=True)
    supersized_fit_always = schema.Bool(
        title=_(u"label_fit_always",
            default=u"Image will never exceed browser width or height. "
                    u"Ignores min. dimensions"),
        default=False)
    supersized_fit_portrait = schema.Bool(
        title=_(u"label_fit_portrait",
            default=u"Portrait images will not exceed browser height"),
        default=True)
    supersized_fit_landscape = schema.Bool(
        title=_(u"label_fit_landscape",
            default=u"Landscape images will not exceed browser width"),
        default=False)
    supersized_thumbnail_navigation = schema.Bool(
        title=_(u"label_thumbnail_navigation",
            default=u"Show next and previous thumb "),
        default=False)
    supersized_thumb_links = schema.Bool(
        title=_(u"label_thumb_links",
            default=u"Individual thumb links for each "
                    u"slide in the 'bottom tray'"),
        default=True)
        
    supersized_disable_click = schema.Bool(
        title=_(u"label_disable_click",
            default=u"Disable clicking on images. "
                    u"Prevents goint to the image if you click on it"),
        default=False)
    supersized_slide_links = schema.Choice(
        title=_(u"label_slide_link",
            default=u"Show slide names in the center of bottom tray (you will "
                    u"need to style 'Name' with css)"),
        default="blank",
        vocabulary=SimpleVocabulary([
            SimpleTerm('name', 'name',
                _(u"label_slide_links_name",
                    default=u"Name")),
            SimpleTerm('blank', 'blank',
                _(u"label_slide_links_blank",
                    default=u"Blank")
            )
        ]))
    supersized_progress_bar = schema.Bool(
        title=_(u"label_progress_bar",
            default=u"Show progress bar"),
        default=False)
    supersized_show_controls = schema.Bool(
        title=_(u"label_show_controls",
            default=u"Hide ALL Controls"),
        default=False)
    supersized_css = schema.Text(
        title=_(u"label_supersized_css",
            default=u"CSS to customize the layout"),
        required=False,
        default=u'#portal-footer {display: none; } body {background: #111; }')


class SupersizedDisplayType(BaseDisplayType):
    name = u"supersized"
    schema = ISupersizedDisplaySettings
    description = _(u"label_supersized_display_type",
        default=u"Supersized")

    def css(self):
        return u"""
        <style>%(supersized_css)s</style>
<link rel="stylesheet" type="text/css"
    href="%(portal_url)s/++resource++ptg.supersized/css/supersized.css"/>
<link rel="stylesheet" type="text/css"
href="%(portal_url)s/++resource++ptg.supersized/theme/supersized.shutter.css"/>
""" % {
    'portal_url': self.portal_url,
    'supersized_css': self.settings.supersized_css
    }

    def javascript(self):
        """  this code looks quite ugly...
        The image part for the javascript is constructed below
        and used in the 'slides' : %(imagelist)s
        """
        images = self.adapter.cooked_images
        imagelist = []
        for image in images:
            image_data = {
                'image': image['image_url'],
                'title': image['title'],
                'thumb': image['thumb_url'],
                }
            if not self.settings.supersized_disable_click:
                image_data['url'] = image['link']

            imagelist.append(image_data)

        return u"""
<script type="text/javascript"
    src="%(portal_url)s/++resource++ptg.supersized/js/supersized.min.js">
</script>
<script type="text/javascript"
src="%(portal_url)s/++resource++ptg.supersized/theme/supersized.shutter.min.js">
</script>
<script type="text/javascript">
jQuery(function($){
$.supersized({
    slideshow: %(slideshow)i, // Slideshow on/off
    autoplay: %(slideshow)i,
    start_slide: 1, // Start slide (0 is random)
    slide_interval: %(speed)i,
    stop_loop: %(stop_loop)i, // Pauses slideshow on last slide
    random: 0, // Randomize slide order (Ignores start slide)
    slide_interval: %(duration)i, // Length between transitions
    // 0-None, 1-Fade, 2-Slide Top, 3-Slide Right, 4-Slide Bottom,
    // 5-Slide Left, 6-Carousel Right, 7-Carousel Left
    transition: %(transition)i,
    transition_speed: %(speed)i, // Speed of transition
    new_window: 0, // Image links open in new window/tab
    pause_hover: 0, // Pause slideshow on hover
    keyboard_nav: 1, // Keyboard navigation on/off
    // 0-Normal, 1-Hybrid speed/quality, 2-Optimizes image quality,
    // 3-Optimizes transition speed // (Only works for Firefox/IE, not Webkit)
    performance: %(performance)i,
    image_protect: 1, // Disables image dragging and right click
    // Size & Position
    min_width: %(min_width)i, // Min width allowed (in pixels)
    min_height: %(min_height)i, // Min height allowed (in pixels)
    vertical_center: %(vertical_center)i, // Vertically center background
    horizontal_center: %(horizontal_center)i, // Horizontally center background
    // Image will never exceed browser width or height (Ignores min. dim)
    fit_always: %(fit_always)i,
    // Portrait images will not exceed browser height
    fit_portrait: %(fit_portrait)i,
    // Landscape images will not exceed browser width
    fit_landscape: %(fit_landscape)i,
    // Components
    // Individual links for each slide (Options: false, 'number',
    // 'name', 'blank')
    slide_links: '%(slide_links)s',
    thumb_links: %(thumb_links)i, // Individual thumb links for each slide
    thumbnail_navigation: %(thumbnail_navigation)i, // Thumbnail navigation
    slides: %(imagelist)s,
    // Theme Options
    image_path: '++resource++ptg.supersized/plone/',
    progress_bar: %(progress_bar)i, // Timer for each slide
    mouse_scrub: 0});
});
</script>
""" % {
        'portal_url': self.portal_url,
        'slideshow': self.settings.supersized_slideshow,
        'stop_loop': self.settings.supersized_stop_loop,
        'min_width': self.settings.supersized_min_width,
        'performance': self.settings.supersized_performance,
        'transition': self.settings.supersized_transition,
        'min_height': self.settings.supersized_min_height,
        'vertical_center': self.settings.supersized_vertical_center,
        'horizontal_center': self.settings.supersized_horizontal_center,
        'fit_always': self.settings.supersized_fit_always,
        'fit_portrait': self.settings.supersized_fit_portrait,
        'fit_landscape': self.settings.supersized_fit_landscape,
        'thumb_links': self.settings.supersized_thumb_links,
        'slide_links': self.settings.supersized_slide_links,
        'thumbnail_navigation': self.settings.supersized_thumbnail_navigation,
        'progress_bar': self.settings.supersized_progress_bar,
        'imagelist': json.dumps(imagelist),
        'speed': self.settings.duration,
        'duration': self.settings.delay,
        }
SupersizedSettings = createSettingsFactory(SupersizedDisplayType.schema)
