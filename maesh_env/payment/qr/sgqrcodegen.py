from payment.qr.qrcodegen import QrCode, QrSegment
import crc16

def generate_qr(amount,UEN,businessName,referenceCode):

	UENLen = "{:02d}".format(len(UEN))
	amountLen = "{:02d}".format(len(amount))
	businessNameLen = "{:02d}".format(len(businessName))
	referenceCodeLen = "{:02d}".format(len(referenceCode))
	referenceCodeRootLen = "{:02d}".format(len(referenceCode) + 4) #The +4 is the 01 in the nested layer and the length of the nested layer i.e. referenceCodeLen

	sgqr = ('00020101021226370009SG.PAYNOW0101202%s%s0301152040000530370254%s%s5802SG59%s%s6009SINGAPORE62%s01%s%s6304' % (UENLen, UEN, amountLen, amount, businessNameLen, businessName, referenceCodeRootLen, referenceCodeLen, referenceCode))

	#sgqr = '00020101021126810011SG.COM.NETS01231198500065G9912312359000211111686614000308686614019908604108C251800007SG.SGQR01121809072DD85C020701.000103060790270402010502060604000007082018091552045812530370254'+digits+amount+'5802SG5912SOBA EXPRESS6009Singapore6304'
	byte_seq = sgqr.encode()
	crc = crc16.crc16xmodem(byte_seq, 0xffff)
	finalcrc = '{:04X}'.format(crc & 0xffff)

	# Numeric mode encoding (3.33 bits per digit)
	qr = QrCode.encode_text(sgqr+finalcrc, QrCode.Ecc.MEDIUM)
	return qr