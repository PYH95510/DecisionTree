package ese589.decisiontree;

public class Attributes {
    public enum WorkClass {
        UNKNOWN("?"),
        PRIVATE("Private"),
        SELF_EMP_INC("Self-emp-inc"),
        SELF_EMP_NOINC("Self-emp-not-inc"), 
        FEDERAL_GOV("Federal-gov"), 
        LOCAL_GOV("Local-gov"), 
        STATE_GOV("State-gov"),
        WITHOUT_PAY("Without-pay"), 
        NEVER_WORKED("Never-worked");

        private final String m_text;

        WorkClass(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static WorkClass fromString(String str) {
            for (WorkClass attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No WorkClass enum constant defined for " + str);
        }
    }
    
    public enum Education {
        BACHELORS("Bachelors"),
        SOME_COLLEGE("Some-college"),
        MASTERS("Masters"),
        DOCTORATE("Doctorate"),
        PRESCHOOL("Preschool"),
        _1_4TH("1st-4th"),
        _5_6TH("5th-6th"),
        _7_8TH("7th-8th"),
        _9TH("9th"),
        _10TH("10th"),
        _11TH("11th"),
        _12TH("12th"),
        HS_GRAD("HS-grad"),
        PROF_SCHOOL("Prof-school"),
        ASSOCIATES_ACDM("Assoc-acdm"),
        ASSOCIATES_VOC("Assoc-voc");

        private final String m_text;

        Education(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Education fromString(String str) {
            for (Education attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Education enum constant defined for " + str);
        }
    }

    public enum MaritalStatus {
        MARRIED_CIV_SPOUSE("Married-civ-spouse"),
        DIVORCED("Divorced"),
        NEVER_MARRIED("Never-married"),
        SEPARATED("Separated"),
        WIDOWED("Widowed"),
        MARRIED_SPOUSE_ABSENT("Married-spouse-absent"),
        MARRIED_AF_SPOUSE("Married-AF-spouse");

        private final String m_text;

        MaritalStatus(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static MaritalStatus fromString(String str) {
            for (MaritalStatus attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No MaritalStatus enum constant defined for " + str);
        }
    }

    public enum Occupation {
        UNKNOWN("?"),
        TECH_SUPPORT("Tech-support"),
        CRAFT_REPAIR("Craft-repair"),
        OTHER_SERVICE("Other-service"),
        SALES("Sales"),
        EXEC_MANAGERIAL("Exec-managerial"),
        PROF_SPECIALTY("Prof-specialty"),
        HANDLERS_CLEANERS("Handlers-cleaners"),
        MACHINE_OP_INSPECT("Machine-op-inspct"),
        ADM_CLERICAL("Adm-clerical"),
        FARMING_FISHING("Farming-fishing"),
        TRANSPORT_MOVING("Transport-moving"),
        PRIV_HOUSE_SERV("Priv-house-serv"),
        PROTECTIVE_SERV("Protective-serv"),
        ARMED_FORCES("Armed-Forces");

        private final String m_text;

        Occupation(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Occupation fromString(String str) {
            for (Occupation attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Occupation enum constant defined for " + str);
        }
    }

    public enum Relationship {
        WIFE("Wife"),
        OWN_CHILD("Own-child"),
        HUSBAND("Husband"),
        NOT_IN_FAMILY("Not-in-family"),
        OTHER_RELATIVE("Other-relative"),
        UNMARRIED("Unmarried");

        private final String m_text;

        Relationship(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Relationship fromString(String str) {
            for (Relationship attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Relationship enum constant defined for " + str);
        }
    }

    public enum Race {
        WHITE("White"),
        ASIAN_PAC_ISLANDER("Asian-Pac-Islander"),
        AMER_INDIAN_ESKIMO("Amer-Indian-Eskimo"),
        OTHER("Other"),
        BLACK("Black");

        private final String m_text;

        Race(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Race fromString(String str) {
            for (Race attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Race enum constant defined for " + str);
        }
    }

    public enum Sex {
        FEMALE("Female"),
        MALE("Male");

        private final String m_text;

        Sex(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Sex fromString(String str) {
            for (Sex attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Sex enum constant defined for " + str);
        }
    }

    public enum NativeCountry {
        UNKNOWN("?"),
        UNITED_STATES("United-States"),
        CAMBODIA("Cambodia"),
        ENGLAND("England"),
        PUERTO_RICO("Puerto-Rico"),
        CANADA("Canada"),
        GERMANY("Germany"),
        OUTLYING_US("Outlying-US(Guam-USVI-etc)"),
        INDIA("India"),
        JAPAN("Japan"),
        GREECE("Greece"),
        SOUTH_KOREA("South"),
        CHINA("China"),
        CUBA("Cuba"),
        IRAN("Iran"),
        HONDURAS("Honduras"),
        PHILLIPINES("Philippines"),
        ITALY("Italy"),
        POLAND("Poland"),
        JAMAICA("Jamaica"),
        VIETNAM("Vietnam"),
        MEXICO("Mexico"),
        PORTUGAL("Portugal"),
        IRELAND("Ireland"),
        FRANCE("France"),
        DOMINICAN_REPUBLIC("Dominican-Republic"),
        LAOS("Laos"),
        ECUADOR("Ecuador"),
        TAIWAN("Taiwan"),
        HAITI("Haiti"),
        COLUMBIA("Columbia"),
        HUNGARY("Hungary"),
        GUATEMALA("Guatemala"),
        NICARAGUA("Nicaragua"),
        SCOTLAND("Scotland"),
        THAILAND("Thailand"),
        YUGOSLAVIA("Yugoslavia"),
        EL_SALVADOR("El-Salvador"),
        TRINADAD_TOBAGO("Trinadad&Tobago"),
        PERU("Peru"),
        HONG_KONG("Hong"),
        HOLAND_NETHERLANDS("Holand-Netherlands");

        private final String m_text;

        NativeCountry(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static NativeCountry fromString(String str) {
            for (NativeCountry attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No NativeCountry enum constant defined for " + str);
        }
    }

    public enum Income {
        MORE50K(">50K"),
        LESS50K("<=50K");

        private final String m_text;

        Income(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Income fromString(String str) {
            for (Income attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Income enum constant defined for " + str);
        }
    }
}
