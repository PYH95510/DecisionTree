package ese589.decisiontree.OtherDataSet;

public class AutismAttribute {

    public enum Jundice {// done
        YES("yes"),
        NO("no");

        private final String m_text;

        Jundice(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Jundice fromString(String str) {
            for (Jundice attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No Education enum constant defined for " + str);
        }
    }

    public enum Autism { // done
        YES("yes"),
        NO("no");

        private final String m_text;

        Autism(String str) {
            m_text = str;
        }

        @Override
        public String toString() {
            return m_text;
        }

        public static Autism fromString(String str) {
            for (Autism attrib : values()) {
                if (attrib.toString().equals(str)) {
                    return attrib;
                }
            }
            throw new IllegalArgumentException("No MaritalStatus enum constant defined for " + str);
        }
    }

    public enum Relationship {// done
        PARENT("Parent"),
        RELATIVE("Relative"),
        SELF("Self"),
        HEALTH_CARE_PROFESSIONAL("Health care professional"),
        OTHERS("Others");

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

    public enum Race { // done
        HISPANIC("Hispanic"),
        BLACK("Black"),
        WHITE_EUROPEAN("White-European"),
        MIDDLE_EASTERN("Middle Eastern"),
        SOUTHASIAN("South Asian"),
        OTHER("Others"),
        LATINO("Latino"),
        ASIAN("Asian");

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

    public enum Sex { // done
        FEMALE("f"),
        MALE("m");

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
        AUSTRIA("Austria"),
        AMERICANSAMOA("AmericanSamoa"),
        UNITED_KINGDOM("United Kingdom"),
        ALBANIA("Albania"),
        BELGIUM("Belgium"),
        AFGHANISTAN("Afghanistan"),
        AUSTRALIA("Australia"),
        BAHRAIN("Bahrain"),
        AZERBAIJAN("Azerbaijan"),
        UNITED_ARAB_EMIRATES("United Arab Emirates"),
        NEW_ZEALAND("New Zealand"),
        UNITED_STATES("United States"),
        ARGENTINA("Argentina"),
        JORDAN("Jordan"),
        CANADA("Canada"),
        BRAZIL("Brazil"),
        CROATIA("Croatia"),
        INDIA("India"),
        BANGLADESH("Bangladesh"),
        FRANCE("France"),
        INDONESIA("Indonesia"),
        EGYPT("Egypt"),
        NETHERLANDS("Netherlands"),
        GREENLAND("Greenland"),
        BAHAMAS("Bahamas"),
        SOUTH_AFRICA("South Africa"),
        VIET_NAM("Viet Nam"),
        COMOROS("Comoros"),
        PORTUGAL("Portugal"),
        FINLAND("Finland"),
        NORWAY("Norway"),
        IRELAND("Ireland"),
        ANGUILLA("Anguilla");

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

}
