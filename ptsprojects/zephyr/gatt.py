"""GATT test cases"""

try:
    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp, MMI
    from ptsprojects.zephyr.qtestcase import QTestCase

except ImportError:  # running this module as script
    import sys
    sys.path.append("../..")  # to be able to locate the following imports

    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp, MMI
    from ptsprojects.zephyr.qtestcase import QTestCase

from ptsprojects.zephyr.iutctl import get_zephyr
import btp


class UUID:
    CEP = '2900'
    CUD = '2901'
    CCC = '2902'
    SCC = '2903'
    CPF = '2904'
    CAF = '2905'
    device_name = '2A00'
    appearance = '2A01'
    battery_level = '2A19'
    date_of_birth = '2A85'
    gender = '2A8C'
    VND16_1 = 'AA50'
    VND16_2 = 'AA51'
    VND16_3 = 'AA52'
    VND16_4 = 'AA53'
    VND16_5 = 'AA54'
    VND128_1 = 'F000BB5004514000B123456789ABCDEF'
    VND128_2 = 'F000BB5104514000B123456789ABCDEF'
    VND128_3 = 'F000BB5204514000B123456789ABCDEF'


def decode_flag_name(flag, names_dict):
    """Returns string description that corresponds to flag"""

    decoded_str = ""
    sep = ", "

    for named_flag in sorted(names_dict.keys()):
        if (flag & named_flag) == named_flag:
            decoded_str += names_dict[named_flag] + sep

    if decoded_str.endswith(sep):
        decoded_str = decoded_str.rstrip(sep)

    return decoded_str


class Prop:
    """Properties of characteresic

    Specified in BTP spec:

    Possible values for the Properties parameter are a bit-wise of the
    following bits:

    0       Broadcast
    1       Read
    2       Write Without Response
    3       Write
    4       Notify
    5       Indicate
    6       Authenticated Signed Writes
    7       Extended Properties

    """
    broadcast     = 2 ** 0
    read          = 2 ** 1
    write_wo_resp = 2 ** 2
    write         = 2 ** 3
    nofity        = 2 ** 4
    indicate      = 2 ** 5
    auth_swrite   = 2 ** 6
    ext_prop      = 2 ** 7

    names = {
        broadcast     : "Broadcast",
        read          : "Read",
        write_wo_resp : "Write Without Response",
        write         : "Write",
        nofity        : "Notify",
        indicate      : "Indicate",
        auth_swrite   : "Authenticated Signed Writes",
        ext_prop      : "Extended Properties",
    }

    @staticmethod
    def decode(prop):
        return decode_flag_name(prop, Prop.names)


class Perm:
    """Permission of characteresic or descriptor

    Specified in BTP spec:

    Possible values for the Permissions parameter are a bit-wise of the
    following bits:

    0       Read
    1       Write
    2       Read with Encryption
    3       Write with Encryption
    4       Read with Authentication
    5       Write with Authentication
    6       Authorization

    """
    read        = 2 ** 0
    write       = 2 ** 1
    read_enc    = 2 ** 2
    write_enc   = 2 ** 3
    read_authn  = 2 ** 4
    write_authn = 2 ** 5
    authz       = 2 ** 6

    names = {
        read        : "Read",
        write       : "Write",
        read_enc    : "Read with Encryption",
        write_enc   : "Write with Encryption",
        read_authn  : "Read with Authentication",
        write_authn : "Write with Authentication",
        authz       : "Authorization"
    }

    @staticmethod
    def decode(perm):
        return decode_flag_name(perm, Perm.names)


def test_cases_server():
    """Returns a list of GATT Server test cases"""

    zephyrctl = get_zephyr()

    test_cases = [
        QTestCase("GATT", "TC_GAC_SR_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF' * 10),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAD_SR_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={17: ("Please confirm IUT receive primary services",
                                    "Service = 0x" + UUID.VND16_1)}),
        QTestCase("GATT", "TC_GAD_SR_BV_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={23: ("Please confirm IUT have following primary services",
                                    "UUID= \'" + UUID.VND16_1 + "\'",
                                    "start handle = 0x0001", "end handle = 0x0001")}),
        QTestCase("GATT", "TC_GAD_SR_BV_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_inc_svc, 1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={24: ("Attribute Handle = 0x0002",
                                    "Included Service Attribute handle = 0x0001",
                                    "End Group Handle = 0x0002",
                                    "Service UUID = 0x" + UUID.VND16_1)}),
        QTestCase("GATT", "TC_GAD_SR_BV_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={25: ("Please confirm IUT have following characteristics",
                                    "UUID= \'" + UUID.VND16_1 + "\'",
                                    "handle=0x0002")}),
        QTestCase("GATT", "TC_GAD_SR_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAD_SR_BV_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read | Perm.write,
                            UUID.VND16_3),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '01234abc'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, 0x00, 0x00,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_02_C",
                  edit1_wids={118: "ffff"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.broadcast, Perm.write, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read | Perm.read_enc,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BV_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND128_1),
                   TestFunc(btp.gatts_set_val, 2, '0123'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_06_C",
                  edit1_wids={111: UUID.VND16_2, 110: "0003"},
                  cmds=[TestFunc(btp.core_reg_svc_gap),
                          TestFunc(btp.core_reg_svc_gatts),
                          TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                          TestFunc(btp.gatts_add_char, 1, 0x00, 0x00,
                                   UUID.VND16_2),
                          TestFunc(btp.gatts_set_val, 2, '01234abc'),
                          TestFunc(btp.gatts_start_server),
                          TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_07_C",
                  edit1_wids={119: UUID.VND16_3},
                  cmds=[TestFunc(btp.core_reg_svc_gap),
                          TestFunc(btp.core_reg_svc_gatts),
                          TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                          TestFunc(btp.gatts_add_char, 1,
                                   Prop.broadcast | Prop.read,
                                   Perm.read | Perm.write, UUID.VND16_2),
                          TestFunc(btp.gatts_set_val, 2, '0123'),
                          TestFunc(btp.gatts_start_server),
                          TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_08_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_11_C",
                  edit1_wids={121: "0003", 122: UUID.VND16_2},
                  cmds=[TestFunc(btp.core_reg_svc_gap),
                          TestFunc(btp.core_reg_svc_gatts),
                          TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                          TestFunc(btp.gatts_add_char, 1, Prop.read,
                                   Perm.read | Perm.read_enc,
                                   UUID.VND16_2),
                          TestFunc(btp.gatts_set_val, 2, '0123'),
                          TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                          TestFunc(btp.gatts_start_server),
                          TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BV_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2,
                            'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={52: ("Please confirm IUT Handle=\'3\'",
                                    "characteristic value=\'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF\'")}),
        QTestCase("GATT", "TC_GAR_SR_BI_12_C",
                  edit1_wids={110: "0003"},
                  cmds=[TestFunc(btp.core_reg_svc_gap),
                          TestFunc(btp.core_reg_svc_gatts),
                          TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                          TestFunc(btp.gatts_add_char, 1, 0x00, 0x00,
                                   UUID.VND16_2),
                          TestFunc(
                              btp.gatts_set_val, 2, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF'),
                          TestFunc(btp.gatts_start_server),
                          TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_13_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2,
                            'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_14_C",
                  edit1_wids={118: "ffff"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read | Prop.write | Prop.nofity,
                               Perm.read | Perm.write, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2,
                               'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_17_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read | Perm.read_enc,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2,
                            'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read | Perm.write,
                            UUID.device_name),
                   TestFunc(btp.gatts_set_val, 2, '0123'),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read | Perm.write,
                            UUID.appearance),
                   TestFunc(btp.gatts_set_val, 4, '4567'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={56: ("Please confirm IUT Handle pair", "0005", "0003", "value=\'45670123\'")}),
        QTestCase("GATT", "TC_GAR_SR_BI_18_C",
                  edit1_wids={110: "0003"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.write, Perm.write, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123'),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read | Prop.write | Prop.nofity,
                               Perm.read | Perm.write, UUID.VND16_3),
                      TestFunc(btp.gatts_set_val, 4, '4567'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_19_C",
                  edit1_wids={118: "ffff"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.write, Perm.write, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123'),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_3),
                      TestFunc(btp.gatts_set_val, 4, '4567'),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read | Prop.write | Prop.nofity,
                               Perm.read | Perm.write, UUID.VND16_4),
                      TestFunc(btp.gatts_set_val, 6, '4567'),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read | Prop.write | Prop.nofity,
                               Perm.read | Perm.write, UUID.VND16_5),
                      TestFunc(btp.gatts_set_val, 8, '4567'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_22_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.appearance),
                   TestFunc(btp.gatts_set_val, 2, '0512'),
                   TestFunc(btp.gatts_add_char, 1, Prop.read,
                            Perm.read | Perm.read_enc, UUID.gender),
                   TestFunc(btp.gatts_set_val, 4, '01'),
                   TestFunc(btp.gatts_set_enc_key_size, 4, 0x0f),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.date_of_birth),
                   TestFunc(btp.gatts_set_val, 6, '20151124'),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.battery_level),
                   TestFunc(btp.gatts_set_val, 8, '10'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BV_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read,
                            UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={52: ("Please confirm IUT Handle=\'4\'", "value=\'FEDCBA9876543210\'")}),
        QTestCase("GATT", "TC_GAR_SR_BI_23_C",
                  edit1_wids={110: "0004"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_add_desc, 2, 0x00, UUID.VND16_3),
                      TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_24_C",
                  edit1_wids={118: "0005"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND128_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_1),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_add_desc, 2, Perm.read,
                               UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_25_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND128_1),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.authz, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_26_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND128_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND128_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.read_authn,
                            UUID.VND128_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_27_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.read_enc, UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_set_enc_key_size, 4, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BV_07_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read,
                            UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4,
                            'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={52: ("Please confirm IUT Handle=\'4\'",
                                    "value=\'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF\'")}),
        QTestCase("GATT", "TC_GAR_SR_BV_08_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(
                       btp.gatts_set_val, 2, '0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABFFFF'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read,
                            UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={52: ("Please confirm IUT Handle=\'3\'",
                                    "value=\'0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABFFFF\'")}),
        QTestCase("GATT", "TC_GAR_SR_BI_28_C",
                  edit1_wids={110: "0004"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_add_desc, 2, 0x00,
                               UUID.VND16_3),
                      TestFunc(
                          btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_29_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read,
                            UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_30_C",
                  edit1_wids={118: "FFFF"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '1234'),
                      TestFunc(btp.gatts_add_desc, 2, Perm.read,
                               UUID.VND16_3),
                      TestFunc(
                          btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_31_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND128_1),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.authz, UUID.VND16_2),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_32_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND128_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND128_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.read_authn, UUID.VND128_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAR_SR_BI_33_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.read_enc, UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_set_enc_key_size, 4, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read | Prop.write_wo_resp,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={75: ("Please confirm IUT Write characteristic handle= '0003'O value= 'BE'O",)}),
        QTestCase("GATT", "TC_GAW_SR_BV_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.auth_swrite,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.auth_swrite,
                            Perm.read | Perm.write | Perm.write_authn,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write, Perm.read | Perm.write,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_02_C",
                  edit1_wids={118: "ffff"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.broadcast | Prop.read | Prop.write_wo_resp,
                               Perm.read | Perm.write, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read, Perm.read,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write | Perm.write_enc,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF' * 10),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_07_C",
                  edit1_wids={118: "ffff"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.broadcast | Prop.read | Prop.write_wo_resp,
                               Perm.read | Perm.write, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_08_C",
                  edit1_wids={120: "0002"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.broadcast | Prop.read, Perm.read,
                               UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        # TODO: fails cause of ZEP-315
        QTestCase("GATT", "TC_GAW_SR_BI_09_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write | Perm.write_enc,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF' * 10),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_13_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read | Perm.write | Perm.write_enc,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF' * 10),
                   TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_10_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.device_name),
                   TestFunc(btp.gatts_set_val, 2, '0123' * 20),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.appearance),
                   TestFunc(btp.gatts_set_val, 4, '4567' * 20),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_14_C",
                  edit1_wids={118: "ffff"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.broadcast | Prop.read | Prop.write,
                               Perm.read | Perm.write, UUID.device_name),
                      TestFunc(btp.gatts_set_val, 2, '0123' * 20),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_15_C",
                  edit1_wids={120: "0002"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.broadcast | Prop.read | Prop.write,
                               Perm.read, UUID.device_name),
                      TestFunc(btp.gatts_set_val, 2, '0123' * 20),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_19_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write,
                            Perm.read | Perm.write | Perm.write_enc,
                            UUID.device_name),
                   TestFunc(btp.gatts_set_val, 2, '0123'),
                   TestFunc(btp.gatts_set_enc_key_size, 2, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_07_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.broadcast | Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.device_name),
                   TestFunc(btp.gatts_set_val, 2, '0123'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_08_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write, UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_20_C",
                  edit1_wids={118: "FFFF"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, 'DCBA'),
                      TestFunc(btp.gatts_add_desc, 2, 0, UUID.VND16_3),
                      TestFunc(btp.gatts_set_val, 4, 'ABCD'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_21_C",
                  edit1_wids={120: "0004"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_add_desc, 2, Perm.read,
                               UUID.VND16_3),
                      TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_22_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND128_1),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.authz, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_23_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND128_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND128_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.write_authn,
                            UUID.VND128_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_24_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.write_enc,
                            UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210'),
                   TestFunc(btp.gatts_set_enc_key_size, 4, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BV_09_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write, UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_25_C",
                  edit1_wids={118: "ABCD"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_add_desc, 2, 0x00,
                               UUID.VND16_3),
                      TestFunc(
                          btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_26_C",
                  edit1_wids={120: "0004"},
                  cmds=[
                      TestFunc(btp.core_reg_svc_gap),
                      TestFunc(btp.core_reg_svc_gatts),
                      TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                      TestFunc(btp.gatts_add_char, 1,
                               Prop.read, Perm.read, UUID.VND16_2),
                      TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                      TestFunc(btp.gatts_add_desc, 2, Perm.read,
                               UUID.VND16_3),
                      TestFunc(
                          btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                      TestFunc(btp.gatts_start_server),
                      TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_27_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write, UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_29_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.authz,
                            UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_30_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.write_authn,
                            UUID.VND16_3),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_31_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.write_enc,
                            UUID.VND16_2),
                   TestFunc(
                       btp.gatts_set_val, 4, 'FEDCBA98765432100123456789ABCDEF0123456789ABCDEF0123456789ABCDEF'),
                   TestFunc(btp.gatts_set_enc_key_size, 4, 0x0f),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_32_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        # TODO: fails cause of ZEP-315
        QTestCase("GATT", "TC_GAW_SR_BI_33_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF' * 5),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_34_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write, UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4, '1234'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAW_SR_BI_35_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '0123456789ABCDEF'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write, UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 4, 'FEDCBA9876543210' * 5),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GAN_SR_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '00'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write, UUID.CCC),
                   TestFunc(btp.gatts_set_val, 2, '01'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GPA_SR_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0001",
                                     "Primary Service = 0x" +
                                     UUID.VND16_1)}),
        QTestCase("GATT", "TC_GPA_SR_BV_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 1, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_3),
                   TestFunc(btp.gatts_add_inc_svc, 1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0001",
                                     "Secondary Service = 0x" +
                                     UUID.VND16_1)}),
        QTestCase("GATT", "TC_GPA_SR_BV_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 1, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_3),
                   TestFunc(btp.gatts_add_inc_svc, 1),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0005",
                                     "Included Service Attribute handle = 0x0001",
                                     "End Group Handle = 0x0003",
                                     "Service UUID = 0x" +
                                     UUID.VND16_1)}),
        QTestCase("GATT", "TC_GPA_SR_BV_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0002",
                                     "Properties = 0x02",
                                     "Handle = 0x0003",
                                     "UUID = 0x" +
                                     UUID.VND16_2)}),
        QTestCase("GATT", "TC_GPA_SR_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.ext_prop,
                            Perm.read | Perm.write, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read, UUID.CEP),
                   TestFunc(btp.gatts_set_val, 4, '0100'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0004",
                                     "Properties = 0x0001")}),
        QTestCase("GATT", "TC_GPA_SR_BV_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read, Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read, UUID.CUD),
                   TestFunc(btp.gatts_set_val, 4, '73616d706c652074657874'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0004",
                                     "User Description = sample text")}),
        QTestCase("GATT", "TC_GPA_SR_BV_07_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1,
                            Prop.read | Prop.write | Prop.nofity,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read | Perm.write,
                            UUID.CCC),
                   TestFunc(btp.gatts_set_val, 4, '0000'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0004",
                                     "Properties = 0x0000")}),
        QTestCase("GATT", "TC_GPA_SR_BV_08_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.broadcast | Prop.read,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2,
                            Perm.read | Perm.write | Perm.write_authn | \
                            Perm.authz, UUID.SCC),
                   TestFunc(btp.gatts_set_val, 4, '0000'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={102: ("Attribute Handle = 0x0004",
                                     "Properties = 0x0000")}),
        QTestCase("GATT", "TC_GPA_SR_BV_11_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read, UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '65'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read, UUID.CPF),
                   TestFunc(btp.gatts_set_val, 4, '04000127010100'),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read, UUID.VND16_3),
                   TestFunc(btp.gatts_set_val, 5, '1234'),
                   TestFunc(btp.gatts_add_desc, 5, Perm.read, UUID.CPF),
                   TestFunc(btp.gatts_set_val, 7, '06001027010200'),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read, UUID.VND16_4),
                   TestFunc(btp.gatts_set_val, 8, '01020304'),
                   TestFunc(btp.gatts_add_desc, 8, Perm.read, UUID.CPF),
                   TestFunc(btp.gatts_set_val, 10, '08001727010300'),
                   TestFunc(btp.gatts_add_char, 1, Prop.read | Prop.write,
                            Perm.read, UUID.VND16_5),
                   TestFunc(btp.gatts_set_val, 11, '65123401020304'),
                   TestFunc(btp.gatts_add_desc, 11, Perm.read, UUID.CAF),
                   TestFunc(btp.gatts_set_val, 13, '040007001000'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)]),
        QTestCase("GATT", "TC_GPA_SR_BV_12_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gatts_add_svc, 0, UUID.VND16_1),
                   TestFunc(btp.gatts_add_char, 1, Prop.read, Perm.read,
                            UUID.VND16_2),
                   TestFunc(btp.gatts_set_val, 2, '1234'),
                   TestFunc(btp.gatts_add_desc, 2, Perm.read, UUID.CPF),
                   TestFunc(btp.gatts_set_val, 4, '0600A327010100'),
                   TestFunc(btp.gatts_start_server),
                   TestFunc(btp.gap_adv_ind_on)],
                  verify_wids={104: ("Value = \'1234\'",
                                     "Attribute Handle = 0x0004",
                                     "Format = 0x06",
                                     "Exponent = 0",
                                     "Uint = 0x27A3",
                                     "Namespace = 0x01",
                                     "Description = 0x0001")}),
    ]

    return test_cases


def test_cases_client(pts_bd_addr):
    """Returns a list of GATT Client test cases

    pts -- Instance of PyPTS

    """
    test_cases = [
        QTestCase("GATT", "TC_GAC_CL_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_exchange_mtu, 0, pts_bd_addr,
                            start_wid=12),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=69),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=69),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # FIXME Verification of data
        # Please confirm IUT receive primary services uuid = '66FA'O ,
        # Service start handle = 0x0001, end handle = 0x0003
        # Service start handle = 0x0030, end handle = 0x0032
        # Service start handle = 0x0040. end handle = 0x0042
        # Service start handle = 0x0050, end handle = 0x0052
        # Service start handle = 0x0090, end handle = 0x0096 in database.
        # Click Yes if IUT receive it, otherwise click No.
        QTestCase("GATT", "TC_GAD_CL_BV_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_disc_prim_uuid, 0, pts_bd_addr,
                            MMI.arg_1, start_wid=18),
                   TestFunc(btp.gattc_disc_prim_uuid_rsp, start_wid=18),
                   TestFunc(btp.gattc_disc_prim_uuid, 0, pts_bd_addr,
                            MMI.arg_1, start_wid=20),
                   TestFunc(btp.gattc_disc_prim_uuid_rsp, start_wid=20),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)],
                  verify_wids={19: btp.verify_description,
                               21: btp.verify_description}),
        # ZEP-336
        # FIXME Verification of data
        # description: Please confirm IUT receive include services:
        # Attribute Handle = 0x0021 Included Service Attribute handle = 0x0040,
        # End Group Handle = 0x0045,Service UUID = 0x5BE7
        #
        # Attribute Handle = 0x0041 Included Service Attribute handle = 0x00A0,
        # End Group Handle = 0x00A2,Service UUID = 0x0EDA
        #
        # Attribute Handle = 0x0061 Included Service Attribute handle = 0x0040,
        # End Group Handle = 0x0045,Service UUID = 0x5BE7
        #
        # Attribute Handle = 0x0062 Included Service Attribute handle = 0x0020,
        # End Group Handle = 0x0026,
        # Service UUID = 0x00003EA1000000000123456789ABCDEF
        #
        # Click Yes if IUT receive it, otherwise click No.
        QTestCase("GATT", "TC_GAD_CL_BV_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   # NOTE: We cannot discover all services at first, so we look
                   # for included at once
                   TestFunc(btp.gattc_find_included, 0, pts_bd_addr, '0001',
                            'FFFF', start_wid=15),
                   TestFunc(btp.gattc_find_included_rsp, start_wid=15),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # ZEP-336
        # FIXME Send command + Verification of data
        # description: Discover all characteristics of service UUID= '180A'O,
        # Service start handle = 0x0030, end handle = 0x0047.
        QTestCase("GATT", "TC_GAD_CL_BV_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_disc_all_chrc, 0, pts_bd_addr, MMI.arg_2,
                            MMI.arg_3, start_wid=27),
                   TestFunc(btp.gattc_disc_all_chrc_rsp, start_wid=27),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # FIXME Verification of data
        # description: Please confirm IUT receive characteristic handle=0x00E5
        # UUID=0x4509  in database. Click Yes if IUT receive it, otherwise
        # click No.
        # PTS issue #14012
        QTestCase("GATT", "TC_GAD_CL_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_disc_chrc_uuid, 0, pts_bd_addr,
                            MMI.arg_1, MMI.arg_2, MMI.arg_3, start_wid=29),
                   TestFunc(btp.gattc_disc_chrc_uuid_rsp, start_wid=29),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # FIXME Verification of data
        # description: Please confirm IUT receive characteristic descriptors
        # handle=0x0013 UUID=0x2902  in database.
        # Click Yes if IUT receive it, otherwise click No.
        QTestCase("GATT", "TC_GAD_CL_BV_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_disc_all_desc, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=31),
                   TestFunc(btp.gattc_disc_all_desc_rsp, start_wid=31),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # handle_mmi_style_yes_no1, 50 "Please confirm IUT receive
        # characteristic value='07'O in random selected adopted database.
        # Click Yes if IUT receive it, othwise click No.
        # \n\nDescription: Verify that the Implementation Under Test (IUT) can
        # send Read characteristic to PTS random select adopted database."
        QTestCase("GATT", "TC_GAR_CL_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # Please confirm IUT receive Invalid handle error. Click Yes if IUT
        # receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # handle_mmi_style_yes_no1, 41 'Please confirm IUT receive read is not
        # permitted error.
        # Click Yes if IUT receive it, othwise click No.\n\nDescription: Verify
        # that the Implementation
        # Under Test (IUT) indicate read is not permitted error when read a
        # characteristic.
        QTestCase("GATT", "TC_GAR_CL_BI_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # Please confirm IUT receive authorization error. Click Yes if IUT
        # receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authentication error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # Please confirm IUT receive encryption key size error. Click Yes if
        # IUT receive it, othwise click No.
        # Description: Verify that the Implementation Under Test (IUT) indicate
        # encryption key size error when read a characteristic.
        QTestCase("GATT", "TC_GAR_CL_BI_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT Handle='b1'O characteristic
        # value='12'O in random selected adopted database.
        # Click Yes if it matches the IUT, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BV_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # Please confirm IUT receive read is not permitted error. Click Yes if
        # IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_12_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Invalid offset error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_13_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_long, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, 1, start_wid=53),
                   TestFunc(btp.gattc_read_long_rsp, start_wid=53),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Invalid handle error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_14_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authorization error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_15_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authentication error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_16_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive encryption key size error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_17_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAR_CL_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_multiple, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAR_CL_BI_18_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_multiple, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAR_CL_BI_19_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_multiple, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAR_CL_BI_20_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_multiple, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAR_CL_BI_21_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_multiple, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAR_CL_BI_22_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read_multiple, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, start_wid=57),
                   TestFunc(btp.gattc_read_multiple_rsp, start_wid=57),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Descriptor value='44'O in
        # random selected adopted database.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BV_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive read is not permitted error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_23_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Invalid handle error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_24_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authorization error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_25_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authentication error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_26_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive encryption key size error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_27_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT Handle='b7'O characteristic
        # value='A600A600'O in random selected adopted database.
        # Click Yes if it matches the IUT, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BV_07_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive read is not permitted error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_28_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Invalid offset error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_29_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=60),
                   TestFunc(btp.gattc_read_rsp, start_wid=60),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Invalid handle error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_30_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authorization error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_31_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive authentication error. Click
        # Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_32_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive encryption key size error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_33_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=58),
                   TestFunc(btp.gattc_read_rsp, start_wid=58),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO
        # description: Please confirm IUT receive Application error. Click Yes
        # if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAR_CL_BI_35_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAW_CL_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_without_rsp, 0, pts_bd_addr,
                            MMI.arg_1, '12', MMI.arg_2, start_wid=70),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Get from MMI data length to be send
        # description: Please send signed write command with handle = '00B1'O
        # with one byte of any octet value to the PTS.
        QTestCase("GATT", "TC_GAW_CL_BV_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_signed_write, 0, pts_bd_addr, MMI.arg_1,
                            '12', None, start_wid=72),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAW_CL_BV_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 61, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid handle error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 62, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write is not permitted error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_03_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 63, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authorization error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_04_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 64, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authentication error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 65, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write encryption key size
        # error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_06_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAW_CL_BV_05_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 61, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid handle error.
        # Click Yes if IUT receive it, othwise click No.
        # PTS issue #14328, #14329
        QTestCase("GATT", "TC_GAW_CL_BI_07_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12' * 23, MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 62, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write is not permitted error.
        # Click Yes if IUT receive it, othwise click No.
        # PTS issue #14328
        QTestCase("GATT", "TC_GAW_CL_BI_08_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 66, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid offset error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_09_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, '12', None, start_wid=77),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=77),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 63, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authorization error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_11_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 64, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authentication error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_12_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 65, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write encryption key size
        # error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_13_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAW_CL_BV_08_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 61, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid handle error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_20_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 62, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write is not permitted error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_21_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 63, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authorization error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_22_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 64, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authentication error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_23_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 65, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write encryption key size
        # error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_24_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAW_CL_BV_09_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 61, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid handle error.
        # Click Yes if IUT receive it, othwise click No.
        # PTS issue #14328
        QTestCase("GATT", "TC_GAW_CL_BI_25_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 62, style: MMI_Style_Yes_No1
        # PTS issue #14328
        # description: Please confirm IUT receive write is not permitted error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_26_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 66, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid offset error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_27_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1,
                            MMI.arg_2, '12', None, start_wid=77),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=77),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # wid: 63, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authorization error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_29_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 64, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write authentication error.
        # Click Yes if IUT receive it, othwise click No.
        # PTS issue #14329
        QTestCase("GATT", "TC_GAW_CL_BI_30_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 65, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive write encryption key size
        # error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_31_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '12', MMI.arg_2, start_wid=76),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=76),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 67, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid attribute value
        # length error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_33_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '1234',
                            MMI.arg_2, start_wid=80),
                   TestFunc(btp.gattc_write_rsp, start_wid=80),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 67, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid attribute value
        # length error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_34_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '1234', MMI.arg_2, start_wid=81),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=81),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 67, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid attribute value
        # length error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_35_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '1234',
                            MMI.arg_2, start_wid=80),
                   TestFunc(btp.gattc_write_rsp, start_wid=80),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # TODO Error Response Verification
        # wid: 67, style: MMI_Style_Yes_No1
        # description: Please confirm IUT receive Invalid attribute value
        # length error.
        # Click Yes if IUT receive it, othwise click No.
        QTestCase("GATT", "TC_GAW_CL_BI_36_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write_long, 0, pts_bd_addr, MMI.arg_1, 0,
                            '1234', MMI.arg_2, start_wid=81),
                   TestFunc(btp.gattc_write_long_rsp, start_wid=81),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        # QTestCase("GATT", "TC_GAN_CL_BV_01_C",
        # QTestCase("GATT", "TC_GAI_CL_BV_01_C",
        QTestCase("GATT", "TC_GAS_CL_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAT_CL_BV_01_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_read, 0, pts_bd_addr, MMI.arg_1,
                            start_wid=48),
                   TestFunc(btp.gattc_read_rsp, start_wid=48),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
        QTestCase("GATT", "TC_GAT_CL_BV_02_C",
                  [TestFunc(btp.core_reg_svc_gap),
                   TestFunc(btp.core_reg_svc_gatts),
                   TestFunc(btp.gap_conn, pts_bd_addr, 0, start_wid=2),
                   TestFunc(btp.gap_connected_ev, pts_bd_addr, 1, start_wid=2),
                   TestFunc(btp.gattc_write, 0, pts_bd_addr, MMI.arg_1, '12',
                            MMI.arg_2, start_wid=74),
                   TestFunc(btp.gattc_write_rsp, start_wid=74),
                   TestFunc(btp.gap_disconn, pts_bd_addr, 0, start_wid=3),
                   TestFunc(btp.gap_disconnected_ev, pts_bd_addr, 1,
                            start_wid=3)]),
    ]

    return test_cases


def test_cases(pts_bd_addr):
    """Returns a list of GATT test cases"""

    test_cases = test_cases_client(pts_bd_addr)
    # test_cases += test_cases_server()

    return test_cases


def main():
    """Main."""
    import sys
    import ptsprojects.zephyr.iutctl as iutctl

    iutctl.init_stub()

    #  to be able to successfully create ZephyrCtl in QTestCase
    iutctl.ZEPHYR_KERNEL_IMAGE = sys.argv[0]

    test_cases_ = test_cases("AB:CD:EF:12:34:56")

    for test_case in test_cases_:
        print
        print test_case

        if test_case.edit1_wids:
            print "edit1_wids: %r" % test_case.edit1_wids

        if test_case.verify_wids:
            print "verify_wids: %r" % test_case.verify_wids

        for index, cmd in enumerate(test_case.cmds):
            str_cmd = str(cmd)

            if isinstance(cmd, TestFunc):
                if cmd.func == btp.gatts_add_char:
                    str_cmd += ", Properties: %s" % Prop.decode(cmd.args[1])
                    str_cmd += ", Permissions: %s" % Perm.decode(cmd.args[2])
                elif cmd.func == btp.gatts_add_desc:
                    str_cmd += ", Permissions: %s" % Perm.decode(cmd.args[1])

            print "%d) %s" % (index, str_cmd)

if __name__ == "__main__":
    main()
