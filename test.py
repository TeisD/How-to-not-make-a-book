from page import Page
from printer import Printer;
import gphoto2 as gp;

printer = Printer();
printer.init();
page = Page(printer.capture());
page.show();
