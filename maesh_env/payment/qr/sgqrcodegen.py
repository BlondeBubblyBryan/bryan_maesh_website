from payment.qr.qrcodegen import QrCode, QrSegment
import crc16

def generate_qr(amount,UEN,businessName,referenceCode):

	UENLen = "{:02d}".format(len(UEN))
	amountLen = "{:02d}".format(len(amount))
	businessNameLen = "{:02d}".format(len(businessName))
	referenceCodeLen = "{:02d}".format(len(referenceCode))
	referenceCodeRootLen = "{:02d}".format(len(referenceCode) + 4) #The +4 is the 01 in the nested layer and the length of the nested layer i.e. referenceCodeLen
	# grabMerchantCode = '36d821d6-2180-42d0-b184-8d5053b212d6'
	# grabMerchantLen = "{:02d}".format(len(grabMerchantCode))
	# grab = '00'+'08'+'com.grab'+'01'+grabMerchantLen+grabMerchantCode
	# grabLen = "{:02d}".format(len(grab))

	id00 = '000201' #Payload Format Indicator
	id01 = '010212' #Point of Initiation Method
	id26 = ('26370009SG.PAYNOW0101202%s%s03011' % (UENLen, UEN)) #SG PayNow
	# id27 = '27810011SG.COM.NETS01231198500065G9912312359000211111510795000308510795019908AC0EE4AB'
	# id51 = '51810007SG.SGQR01121809052DD729020700.00010306408897040201050315906040000070820180905'
	id52 = '52040000' #Merchant Category Code
	id53 = '5303702' #Transaction Currency
	id54 = ('54%s%s' % (amountLen, amount)) # Amount
	id58 = '5802SG' #Country Code
	id59 = ('59%s%s' % (businessNameLen, businessName)) #Merchant Name
	id60 = '6009SINGAPORE' #Merchant City
	id62 = ('62%s01%s%s' % (referenceCodeRootLen, referenceCodeLen, referenceCode)) #Reference code
	id63 = '6304' #CRC

	sgqr = id00 + id01 + id26 + id52 + id53 + id54 + id58 + id59 + id60 + id62 + id63

	# sgqr = '00020101021126810011SG.COM.NETS01231198500065G9912312359000211111686614000308686614019908604108C251800007SG.SGQR01121809072DD85C020701.00010306079027040201050206060400000708201809155204581253037025802SG5912SOBC EXPRESS6009Singapore6304'
	byte_seq = sgqr.encode()
	crc = crc16.crc16xmodem(byte_seq, 0xffff)
	finalcrc = '{:04X}'.format(crc & 0xffff)

	# Numeric mode encoding (3.33 bits per digit)
	qr = QrCode.encode_text(sgqr+finalcrc, QrCode.Ecc.MEDIUM)
	return qr