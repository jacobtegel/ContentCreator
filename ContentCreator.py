# menuTitle: Content Creator

"""
Little helper script to quickly create simple font graphics for social media, without having to touch some layout software. 
If Font is not installed, it will be test installed.

Jacob Tegel 2025
"""

from vanilla import *
from AppKit import NSColor, NSButton, NSFontManager
from mojo.UI import Message
import drawBot
from drawBot.ui.drawView import DrawView
import traceback
import os
from datetime import datetime

time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

f = CurrentFont()

if f is None:
    Message("Please open a font in RoboFont.")

else:
    familyName = f.info.familyName.replace(" ", "")
    styleName = f.info.styleName.replace(" ", "")
    fontName = familyName + "-" + styleName
    
installedFonts = NSFontManager.sharedFontManager().availableFonts()

if fontName not in installedFonts:
    f.testInstall()

class Controller:
    def __init__(self):
        self.winWidth = 1200
        self.winHeight = 800
        self.sidebarWidth = 300

        self.w = Window((self.winWidth, self.winHeight), "Content Creator", (100, 100))
        self.w.controls = Group((-self.sidebarWidth, 10, self.sidebarWidth, -10))

        x1 = 10
        x2 = 100
        y = 10
        dy = 35
        w1 = 80
        w2 = -10
        h = 25
        
        self.w.controls.fontCheck = CheckBox((x1, y, w1+70, h), "Use Current Font", callback=self.fontCheck, value=True)
        y += dy
        
        self.w.controls.fontLabel = TextBox((x1, y, w1, h), "Font:")
        self.w.controls.fontName = TextBox((x2, y, w2, h), f"{f.info.familyName} {f.info.styleName}")
        self.w.controls.fontDropdown = PopUpButton((x2, y, w2, h), installedFonts, callback=self.redraw)
        self.w.controls.fontDropdown.show(False)
        y += dy
        
        self.w.controls.layoutText = TextBox((x1, y, w1, h), "Layout:")
        self.w.controls.layout = PopUpButton((x2, y, w2, h), ["1×1", "4×5", "9×16", "DIN A4"], callback=self.redraw)
        y += dy

        self.w.controls.marginText = TextBox((x1, y, w1, h), "Margin:")
        self.w.controls.marginSlider = Slider((x2, y, w2-50, h), minValue=0, maxValue=100, value=10, callback=self.marginSliderChanged)
        self.w.controls.marginValue = EditText((w2-45, y, w2, h), str(round(float(self.w.controls.marginSlider.get()), 1)), callback = self.marginValueChanged)
        y += dy

        self.w.controls.txtText = TextBox((x1, y, w1, h), "Text:")
        self.w.controls.txt = TextEditor((x2, y, w2, h*2), "Sample Text", callback=self.redraw)
        y += dy + h

        self.w.controls.alignText = TextBox((x1, y, w1, h), "Alignment:")
        self.w.controls.align = PopUpButton((x2, y, w2, h), ["Left", "Center", "Right", "Justified"], callback=self.redraw)
        y += dy
        
        self.w.controls.vertAlignText = TextBox((x1, y, w1, h), "Vertical:")
        self.w.controls.vertAlign = PopUpButton((x2, y, w2, h), ["Top", "Center", "Bottom"], callback=self.redraw)
        y += dy

        self.w.controls.fSizeText = TextBox((x1, y, w1, h), "Font Size:")
        self.w.controls.fSizeSlider = Slider((x2, y, w2-50, h), minValue=10, maxValue=1000, value=100, callback=self.fSizeSliderChanged)
        self.w.controls.fSizeValue = EditText((w2-45, y, w2, h), str(round(float(self.w.controls.fSizeSlider.get()), 1)), callback = self.fSizeValueChanged)
        y += dy
        
        self.w.controls.lHeightText = TextBox((x1, y, w1, h), "Line Height:")
        self.w.controls.lHeightSlider = Slider((x2, y, w2-45, h), minValue=.8, maxValue=2, value=1.2, tickMarkCount=None, callback=self.lHeightSliderChanged)
        self.w.controls.lHeightValue = EditText((w2-40, y, w2, h), str(round(float(self.w.controls.lHeightSlider.get()), 2)), callback = self.lHeightValueChanged)
        y += dy

        self.w.controls.tColText = TextBox((x1, y, w1, h), "Text Color:")
        self.w.controls.tCol = ColorWell((x2, y, w2, h+10), callback=self.redraw, color=NSColor.redColor())
        y += dy + 10

        self.w.controls.bColText = TextBox((x1, y, w1, h), "Background Color:")
        self.w.controls.bCol = ColorWell((x2, y, w2, h+10), callback=self.redraw, color=NSColor.whiteColor())
        y += dy + 10
    
        self.w.controls.exportText = TextBox((x1, y, w1, h), "Export as:")
        self.w.controls.exportPdf = CheckBox((x2, y, w2, h), "PDF", callback=self.redraw)
        y += dy -10
        self.w.controls.exportSvg = CheckBox((x2, y, w2, h), "SVG", callback=self.redraw)
        y += dy -10
        self.w.controls.exportPng = CheckBox((x2, y, w2, h), "PNG", callback=self.redraw)
        y += dy
        
        self.w.controls.pathControl = PathControl((x1, y+2.5, self.sidebarWidth / 2 - 25, h), None, pathStyle="popUp", callback=self.pathControlCallback)
        self.w.controls.exportButton = Button((self.sidebarWidth / 2, y, self.sidebarWidth / 2 - 25, h), "Export", callback=self.exportButtonCallback)

        self.w.preview = DrawView((10, 10, -self.sidebarWidth-10, -10))

        self.w.open()
        self.redraw(None)

    def fontCheck(self, sender):
        if self.w.controls.fontCheck.get() == 1:
            self.w.controls.fontName.show(True)
            self.w.controls.fontDropdown.show(False)
        else:
            self.w.controls.fontName.show(False)
            self.w.controls.fontDropdown.show(True)
        self.redraw(sender)

    def marginSliderChanged(self, sender):
        v = round(float(self.w.controls.marginSlider.get()), 1)
        self.w.controls.marginValue.set(str(v))
        self.redraw(sender)
    
    def marginValueChanged(self, sender):
        v = round(float(self.w.controls.marginValue.get()), 1)
        self.w.controls.marginSlider.set(v)
        self.redraw(sender)
        
    def fSizeSliderChanged(self, sender):
        v = round(float(self.w.controls.fSizeSlider.get()), 1)
        self.w.controls.fSizeValue.set(str(v))
        self.redraw(sender)
    
    def fSizeValueChanged(self, sender):
        v = round(float(self.w.controls.fSizeValue.get()), 1)
        self.w.controls.fSizeSlider.set(v)
        self.redraw(sender)
        
    def lHeightSliderChanged(self, sender):
        v = round(float(self.w.controls.lHeightSlider.get()), 2)
        self.w.controls.lHeightValue.set(str(v))
        self.redraw(sender)
    
    def lHeightValueChanged(self, sender):
        v = round(float(self.w.controls.lHeightValue.get()), 2)
        self.w.controls.lHeightSlider.set(v)
        self.redraw(sender)
    
    def pathControlCallback(self, sender):
        # url = self.w.controls.pathControl.get()
        
        # if url and not os.path.isdir(url):
        #     sender.set(None)
        #     self.showMessage("Error.", "The path must be a folder.")
        
        self.redraw(sender)
        
    def exportButtonCallback(self, sender):
        self.redraw(sender)
        self.export(sender)
        
    def getUI(self):
        
        fontDropdown = installedFonts[self.w.controls.fontDropdown.get()]

        layoutChoice = self.w.controls.layout.getTitle()
        
        if layoutChoice == "1×1":
            artboard = (1080, 1080)
        elif layoutChoice == "4×5":
            artboard = (1080, int(1080 / 4 * 5))
        elif layoutChoice == "9×16":
            artboard = (1080, int(1080 / 9 * 16))
        elif layoutChoice == "DIN A4":
            artboard = "A4"
        else:
            artboard = (1080, 1080)
        
        margin = self.w.controls.marginSlider.get()
        txt = self.w.controls.txt.get()
        alignment = self.w.controls.align.get()
        vertAlign = self.w.controls.vertAlign.get()
        
        fSize = self.w.controls.fSizeSlider.get()
        lHeight = self.w.controls.lHeightSlider.get()
        
        tCol = self.w.controls.tCol.get()
        bCol = self.w.controls.bCol.get()
        
        exportPdf = self.w.controls.exportPdf.get()
        exportSvg = self.w.controls.exportSvg.get()
        exportPng = self.w.controls.exportPng.get()

        url = self.w.controls.pathControl.get()
        
        exportButton = self.w.controls.exportButton.getNSButton()
        
        return artboard, fontDropdown, margin, txt, alignment, vertAlign, fSize, lHeight, tCol, bCol, exportPdf, exportSvg, exportPng, url

    def redraw(self, sender):
        artboard, fontDropdown, margin, text, alignment, vertAlign, fSize, lHeight, tCol, bCol, exportPdf, exportSvg, exportPng, url = self.getUI()
                
        drawBot.newDrawing()
        
        # try:
        #     drawBot.fallbackFont("AND-Regular")
        # except Exception as e:
        #     print(e)            
        
        if isinstance(artboard, str):
            drawBot.newPage(artboard)
        else:
            drawBot.newPage(*artboard)

        w, h = drawBot.width(), drawBot.height()
        
        drawBot.fill(bCol)
        
        drawBot.rect(0, 0, w, h)
        
        # print(fontName)
        if self.w.controls.fontCheck.get() == 1:
            drawBot.font(fontName)
        else:
            drawBot.font(fontDropdown)
        
        drawBot.fontSize(fSize)
        drawBot.lineHeight(fSize * lHeight)
        
        tw, th = drawBot.textSize(text, width=(w - margin))
        
        x, y = (w / 2) - (tw / 2), (h / 2) - (th / 2)
        
        drawBot.fill(tCol)
        
        if alignment == 0:
            alignment = "left"
        elif alignment == 1:
            alignment = "center"
        elif alignment == 2:
            alignment = "right"
        elif alignment == 3:
            alignment = "justified"
        
        if vertAlign == 0:
            x, y, w, h = 0 + margin/2 , drawBot.height() - th - margin/2, drawBot.width() - margin, th
        elif vertAlign == 1:
            x, y, w, h = 0 + margin/2, y, drawBot.width() - margin, th
        elif vertAlign == 2:
            x, y, w, h = 0 + margin / 2, 0 + margin / 2, drawBot.width() - margin, th
        
        drawBot.textBox(text, (x, y, w, h), align = alignment)
        
        pdf = drawBot.pdfImage()
        
        self.w.preview.setPDFDocument(pdf)

        drawBot.endDrawing()

    def export(self, sender):
        url = self.w.controls.pathControl.get()
        exportPdf = self.w.controls.exportPdf.get()
        exportSvg = self.w.controls.exportSvg.get()
        exportPng = self.w.controls.exportPng.get()        
        
        if url is None or not os.path.isdir(url):
            Message("Please select a destination folder.")
            return
        
        export = f"{url}/ContentCreator" 
                
        try:
            if not os.path.exists(export):
                os.makedirs(export)
            
            if exportPdf:
                drawBot.saveImage(f"{export}/{time}-ContentCreator-{fontName}.pdf")
            if exportSvg:
                drawBot.saveImage(f"{export}/{time}-ContentCreator-{fontName}.svg")
            if exportPng:
                drawBot.saveImage(f"{export}/{time}-ContentCreator-{fontName}.png", imageResolution=300)
        except Exception as e:
            Message(f"Export Failed", e, traceback.format_exc())
            

Controller()