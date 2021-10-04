
import fitz
import os, shutil
from paddleocr import PaddleOCR

class TextDetect:

    def __init__(self, pdfPath, imgPath, zoom_x, zoom_y):

        # Initialize dictionary
        self.textDict = {   'commodityType': '',
                            'futureCommodityType': '',
                            'entrustSubject': '',
                            'operatorName': '',
                            'commodityMark': '',
                            'contractId': '',
                            'marginSize': '',
                            'marginDefaultRatio': '',
                            'spotPositionDirection': '',
                            'futuresPositionDirection': '',
                            'openingPrice': '',
                            'priceTop': '',
                            'spotQuantity': '',
                            'futuresQuantity': '',
                            'hedgeRatio': '',
                            'maxLossLimit': '',
                            'targetStopLossPosition': '',
                            'targetStopPosition': '',
                            'quotationsAnalysis': '',
                            'positionPlan': '',
                            'liquidationPlan': '',
                            'remark': ''  }
        self.pdfPath = pdfPath
        self.imgPath = imgPath
        self.zoom_x = zoom_x
        self.zoom_y = zoom_y


    # split pdf document into several pages, where each page is stored as an image under the 'pdfs' folder
    def pdf2image(self):
        # open pdf document
        pdf = fitz.open(self.pdfPath)

        if not os.path.exists(self.imgPath):# check if folder exists
                os.mkdir(self.imgPath) # if not exist then create one
        else:
            # if the folder already exists, then empty it and store current images
            for f in os.listdir(self.imgPath):
                filePath = os.path.join(self.imgPath, f)
                if os.path.isfile(filePath):
                    os.remove(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)

        # read pdf page by page
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            # set zooming & rotating params
            trans = fitz.Matrix(self.zoom_x, self.zoom_y).preRotate(0)
            pm = page.getPixmap(matrix=trans, alpha=False)
        
            # write images
            pm.writePNG(self.imgPath+'/'+str(pg)+".png")

        pdf.close()


    # extract info on the first page of pdf
    def convertText1(self, img):

        ocr = PaddleOCR() # need to run only once to download and load model into memory
        result = ocr.ocr(img) # return a list with coordinates, content and accuracy

        index = 0
        done = False
        for line in result:
            if done: break
            [corList, (txt, _)] = line
            [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] = corList
            if txt == '委托主体名称':
                [corListPrev, (txtP, _)] = result[index-1]
                [corListAft, (txtA, _)] = result[index+1]
                [[_,yp1], _, _, _] = corListPrev
                [[_,ya1], _, _, _] = corListAft
                if abs(yp1-y1) < abs(ya1-y1):
                    self.textDict['entrustSubject'] = txtP
                else:
                    self.textDict['entrustSubject'] = txtA
            elif txt == '操作主体名称':
                [corListPrev, (txtP, _)] = result[index-1]
                [corListAft, (txtA, _)] = result[index+1]
                [[_,yp1], _, _, _] = corListPrev
                [[_,ya1], _, _, _] = corListAft
                if abs(yp1-y1) < abs(ya1-y1):
                    self.textDict['operatorName'] = txtP
                else:
                    self.textDict['operatorName'] = txtA
            elif '现货品种' in txt:
                self.findContent1(index, y1, y4, x2, result, '现货品种')
            elif '开仓价格' in txt:
                self.findContent1(index, y1, y4, x2, result, '开仓价格')
                done = True

            index += 1


    # extract info from page 2
    def convertText2(self, img):

        ocr = PaddleOCR() # need to run only once to download and load model into memory
        result = ocr.ocr(img) # return a list with coordinates, content and accuracy

        index = 0
        done = False
        for line in result:
            if done: break
            [corList, (txt, _)] = line
            [[_,y1], [x2,_], [_,_], [_,y4]] = corList
            if '期货品种' in txt:
                self.findContent2(index, y1, y4, x2, result, '期货品种')
            elif '现货头寸' in txt:
                self.findContent2(index, y1, y4, x2, result, '现货头寸')
            elif '期货头寸' in txt:
                self.findContent2(index, y1, y4, x2, result, '期货头寸')
            elif '现货数量' in txt:
                self.findContent2(index, y1, y4, x2, result, '现货数量')
            elif '手' in txt:
                self.findContent2(index, y1, y4, x2, result, '合约数量')
            elif '计划套保' in txt:
                [corListPrev, (txtP, _)] = result[index-1]
                [corListAft, (txtA, _)] = result[index+1]
                [[_,yp1], _, _, _] = corListPrev
                [[_,ya1], _, _, _] = corListAft
                if abs(yp1-y1) < abs(ya1-y1):
                    self.textDict['hedgeRatio'] = txtP
                else:
                    self.textDict['hedgeRatio'] = txtA
            elif '保证金规模' in txt:
                self.findContent2(index, y1, y4, x2, result, '保证金规模')
            elif txt == '最大亏损限额':
                self.findContent2(index, y1, y4, x2, result, '最大亏损')
            elif txt == '行情分析':
                self.get_multi_lines(index, result, '行情分析')
            elif txt == '持仓预案':
                self.get_multi_lines(index, result, '持仓预案')
            elif txt == '平仓预案':
                self.get_multi_lines(index, result, '平仓预案')
            elif '止盈位' in txt:
                self.get_multi_lines(index, result, '止盈')
            elif '止损位' in txt:
                self.get_multi_lines(index, result, '止损')
            elif '备注' in txt:
                self.get_multi_lines(index, result, '备注')
                done = True
                
            index += 1


    # check 3 positions ahead of and below the current table title to find the corresponding content for the title
    def findContent1(self, index, top, bottom, right, result, txt):

        text = ''

        [corListP1, (txtP1, _)] = result[index-3]
        [corListP2, (txtP2, _)] = result[index-2]
        [corListP3, (txtP3, _)] = result[index-1]
        [corListA1, (txtA1, _)] = result[index+1]
        [corListA2, (txtA2, _)] = result[index+2]
        [corListA3, (txtA3, _)] = result[index+3]

        [[xp1,yp1], _, _, _] = corListP1
        [[xp2,yp2], _, _, _] = corListP2
        [[xp3,yp3], _, _, _] = corListP3
        [[xa1,ya1], _, _, _] = corListA1
        [[xa2,ya2], _, _, _] = corListA2
        [[xa3,ya3], _, _, _] = corListA3

        Y = [yp1, yp2, yp3, ya1, ya2, ya3]
        X = [xp1, xp2, xp3, xa1, xa2, xa3]

        # clean content that doesn't stay in target line
        disY = abs(bottom - top)
        yList, xList = [], []
        index = 0
        for cor in Y:
            if abs(cor-top) < (disY/2):
                yList.append(cor)
                xList.append(X[index])
            index += 1

        # look for the content that is closet to the table title horinzontally
        xmin = 0
        disF = xList[0]
        for x_ in xList:
            dis = abs(x_-right)
            if dis < disF:
                disF = dis
                xmin = x_

        if xmin == xp1:
            text = txtP1
        elif xmin == xp2:
            text = txtP2
        elif xmin == xp3:
            text = txtP3
        elif xmin == xa1:
            text = txtA1
        elif xmin == xa2:
            text = txtA2
        elif xmin == xa3:
            text = txtA3

        if txt == '现货品种':
            self.textDict['commodityType'] = text
            self.textDict['commodityMark'] = text
        elif txt == '开仓价格':
            self.textDict['openingPrice'] = text


    # Also check 3 positions ahead of and below the current table title in the second page
    def findContent2(self, index, top, bottom, right, result, txt):

        text = ''

        [corListP1, (txtP1, _)] = result[index-3]
        [corListP2, (txtP2, _)] = result[index-2]
        [corListP3, (txtP3, _)] = result[index-1]
        [corListA1, (txtA1, _)] = result[index+1]
        [corListA2, (txtA2, _)] = result[index+2]
        [corListA3, (txtA3, _)] = result[index+3]

        [[xp1,yp1], _, _, _] = corListP1
        [[xp2,yp2], _, _, _] = corListP2
        [[xp3,yp3], _, _, _] = corListP3
        [[xa1,ya1], _, _, _] = corListA1
        [[xa2,ya2], _, _, _] = corListA2
        [[xa3,ya3], _, _, _] = corListA3

        Y = [yp1, yp2, yp3, ya1, ya2, ya3]
        X = [xp1, xp2, xp3, xa1, xa2, xa3]

        # clean content that doesn't stay in target line
        disY = abs(bottom - top)
        yList, xList = [], []
        index = 0
        for cor in Y:
            if abs(cor-top) < (disY/2):
                yList.append(cor)
                xList.append(X[index])
            index += 1

        # look for the content that is closet to the table title horinzontally
        xmin = 0
        disF = xList[0]
        for x_ in xList:
            dis = abs(x_-right)
            if dis < disF:
                disF = dis
                xmin = x_

        if xmin == xp1:
            text = txtP1
        elif xmin == xp2:
            text = txtP2
        elif xmin == xp3:
            text = txtP3
        elif xmin == xa1:
            text = txtA1
        elif xmin == xa2:
            text = txtA2
        elif xmin == xa3:
            text = txtA3

        if txt == '期货品种':
            self.textDict['futureCommodityType'] = text
            self.textDict['contractId'] = text
        elif txt == '现货头寸':
            self.textDict['spotPositionDirection'] = text
        elif txt == '期货头寸':
            self.textDict['futuresPositionDirection'] = text
        elif txt == '现货数量':
            self.textDict['spotQuantity'] = text
        elif txt == '合约数量':
            self.textDict['futuresQuantity'] = text
        elif txt == '保证金规模':
            self.textDict['marginSize'] = text
        elif txt == '最大亏损':
            self.textDict['maxLossLimit'] = text


    # get position info of the line before table title
    # If found content, return that line's bottom coordinate
    def get_upper_bound(self, index, num, result):

        coords = []
        for i in range(1, num+1):
            [corList, (txt, _)] = result[index-i]
            [[x1,y1], _, _, [x4,y4]] = corList
            coords.append((y1, y4))
        (y1, y2) = coords[0]
        disWord = abs(y1-y2)

        # look for min bottom coordinate ahead of table title and make it the top coordinate of target content (correspond to the current table title)
        # locate distance between lines to distinguish info on the same line from the previous line
        # If found min bottom coordinate and second min bottom coordinate, then if the distance between them is less than 1.7 (height of character), treat them as in the same table cell, return 0
        # otherwise return the min bottom coordinate
        bottomMin = bottomSec = y2
        coordF = coordS = (y1, y2)
        for (top, bottom) in coords:
            if bottom < bottomMin:
                if bottomMin < bottomSec:
                    bottomSec = bottomMin
                    coordS = coordF
                bottomMin = bottom
                coordF = (top, bottom)
            elif bottom < bottomSec:
                bottomSec = bottom
                coordS = (top, bottom)
        (_, bottom_) = coordF
        (top_, _) = coordS
        if abs(top_-bottom_) >= (disWord/1.7):
            return bottom_
        else:
            return 0


    # get position info of the next line after table title
    # If found content, return that line's top coordinate
    def get_lower_bound(self, index, num, result):

        coords = []
        for i in range(1, num+1):
            [corList, (txt, _)] = result[index+i]
            [[x1,y1], _, _, [x4,y4]] = corList
            coords.append((y1, y4))
        (y1, y2) = coords[0]
        disWord = abs(y1-y2)

        # look for max top coordinate ahead of table title and make it the bottom coordinate of target content (correspond to the current table title)
        # locate distance between lines to distinguish info on the same line from the previous line
        # If found max top coordinate and second max top coordinate, then if the distance between them is less than 1.7 (height of character), treat them as in the same table cell, return 0
        # otherwise return the max top coordinate
        bottomMax = bottomSec = y2
        coordF = coordS = (y1, y2)
        for (top, bottom) in coords:
            if bottom > bottomMax:
                if bottomMax < bottomSec:
                    bottomSec = bottomMax
                    coordS = coordF
                bottomMax = bottom
                coordF = (top, bottom)
            elif bottom > bottomSec:
                bottomSec = bottom
                coordS = (top, bottom)
        (top_, _) = coordF
        (_, bottom_) = coordS
        if abs(top_-bottom_) >= (disWord/1.7):
            return top_
        else:
            return 0


    def has_upper_bound(self, index, result):

        [corList, (txt, _)] = result[index]
        [[_,up1], _, _, [_,down1]] = corList
        [corList, (txt, _)] = result[index-1]
        [[_,up2], _, _, [_,down2]] = corList
        disY = abs(up1-down1)
        if abs(down2-up1) <= (disY/2) or abs(up1-up2) <= (disY/2):
            return True
        return False


    def has_lower_bound(self, index, result):

        [corList, (txt, _)] = result[index]
        [[_,up1], _, _, [_,down1]] = corList
        [corList, (txt, _)] = result[index+1]
        [[_,up2], _, _, [_,down2]] = corList
        disY = abs(up1-down1)
        if abs(down1-down2) <= (disY/2) or abs(down1-up2) <= (disY/2):
            return True
        return False


    # get multple lines correspond to the current table title
    def get_multi_lines(self, index, result, word):

        text = ''
        [corList1, (txt1, _)] = result[index]
        [_, [right,_], _, _] = corList1

        if self.has_upper_bound(index, result):
            numB = 2
            # if return is 0, then it means haven't found the upper bound
            while (self.get_upper_bound(index, numB, result) == 0):
                numB += 1
            upper = self.get_upper_bound(index, numB, result)
            for i in reversed(range(1, numB+1)):
                [corList, (txt, _)] = result[index-i]
                [[x1,_], _, _, [x4,y4]] = corList
                # locate in the same cell as table title and is on th right of it
                if y4 > upper and x1 > right:
                    text += txt
        
        if self.has_lower_bound(index, result):
            numU = 2
            # if return is 0, then it means haven't found the lower bound
            while (self.get_lower_bound(index, numU, result) == 0):
                numU += 1
            lower = self.get_lower_bound(index, numU, result)
            for i in range(1, numU+1):
                [corList, (txt, _)] = result[index+i]
                [[x1,y1], _, _, _] = corList
                # lcoate in the same cell as table title and is on the right of it
                if y1 < lower and x1 > right:
                    text += txt

        if word == '行情分析':
            self.textDict['quotationsAnalysis'] = text
        elif word == '持仓预案':
            self.textDict['positionPlan'] = text
        elif word == '平仓预案':
            self.textDict['liquidationPlan'] = text
        elif word == '止盈':
            self.textDict['targetStopPosition'] = text
        elif word == '止损':
            self.textDict['targetStopLossPosition'] = text
        elif word == '备注':
            self.textDict['remark'] = text
        
    
    # update dict to fill in the info we extract
    def get_dict(self):
        self.pdf2image()
        self.convertText1("pdfs/0.png")
        self.convertText2("pdfs/1.png")
        with open("sample/sample_result.txt", 'w') as code:
            code.write(str(self.textDict))


if __name__ == '__main__':
    # read from pdf document
    pdfPath = "sample/sample_pdf.pdf"
    text = TextDetect(pdfPath, 'pdfs', 8, 8)
    text.get_dict()
