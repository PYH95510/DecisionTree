package ese589.decisiontree;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public class AttributeSelection {
    public static class Entropy {
        private static float entropy(float value) {
            return -value * (float)Math.log(value) / (float)Math.log(2);
        }

        public static <EL extends Enum<EL>> float forClass(Class<EL> classEnumType, List<EL> classEntries) {
            int numClassTypes = classEnumType.getEnumConstants().length;
            int[] count = new int[numClassTypes];
            for (EL class_ : classEntries) {
                count[class_.ordinal()] += 1;
            }
            float entropy = 0;
            for (int i = 0; i < numClassTypes; ++i) {
                if (count[i] <= 0) continue;
                entropy += entropy((float)count[i] / classEntries.size());
            }
            return entropy;
        }

        public static <EC extends Enum<EC>, EA extends Enum<EA>> float forAttribDiscrete(
            Class<EC> classEnumType, 
            Class<EA> attribEnumType, 
            List<EC> classes, 
            List<EA> attribs) 
        {
            assert(classes.size() == attribs.size());

            int numAttribTypes = attribEnumType.getEnumConstants().length;
            int numClassTypes = classEnumType.getEnumConstants().length;

            // "counts" 2-D array keeps the counts for combinations of values of attribute and values of class
            // Example:
            // For an attribute "Education", the following are the possible values:
            //  HIGH_SCHOOL
            //  COLLEGE
            //  GRADUATE
            // and the followning are the possible values of class "Income":
            //  <=50K
            //  >50K
            // The "counts" array would be size of 3 x 2 and will keep the counts for ocurrence of each permutation of these values
            int[][] counts = new int[numAttribTypes][numClassTypes];
            for (int i = 0; i < classes.size(); ++i) {
                counts[attribs.get(i).ordinal()][classes.get(i).ordinal()] += 1;
            }

            int totalCount = attribs.size();
            float entropy = 0;
            // For each attributes
            for (int i = 0; i < numAttribTypes; ++i) {
                int attribValCount = 0;
                // Count number of occurences for each attribute value
                for (int j = 0; j < numClassTypes; ++j) {
                    attribValCount += counts[i][j];
                }
                for (int j = 0; j < numClassTypes; ++j) {
                    if (counts[i][j] <= 0) continue;
                    entropy += (float)attribValCount / totalCount * (entropy((float)counts[i][j] / attribValCount));
                }
            }
            return entropy;
        }

        static class ClassAttribPair<EC extends Enum<EC>, EA> {
            EC class_;
            EA attrib;
        }

        static class AttribPair<EA> {
            EA left;
            EA right;
        }

        public static <EC extends Enum<EC>, EA> AttribPair<EA> forAttribContinuous(
            Class<EC> classEnumType,
            List<EC> classes, 
            List<EA> attribs, 
            Comparator<EA> ascendComp) 
        {
            assert(classes.size() == attribs.size());

            ArrayList<ClassAttribPair<EC, EA>> classAttribList = new ArrayList<>(classes.size());
            for (int i = 0; i < classes.size(); ++i) {
                var classAttribPair = new ClassAttribPair<EC, EA>();
                classAttribPair.class_ = classes.get(i);
                classAttribPair.attrib = attribs.get(i);
                classAttribList.add(classAttribPair);
            }
            classAttribList.sort(new Comparator<ClassAttribPair<EC, EA>>() {
                @Override
                public int compare(ClassAttribPair<EC, EA> arg0, ClassAttribPair<EC, EA> arg1) {
                    return ascendComp.compare(arg0.attrib, arg1.attrib);
                }
            });

            int numClassTypes = classEnumType.getEnumConstants().length;

            // Try with every unique bisections of the set
            // Keep track of which bisection has the least entropy
            float minEntropy = Float.POSITIVE_INFINITY;
            int minPartitionIdx = -1;
            for (int i = 1; i < attribs.size(); ++i) {
                float entropy = 0;
                int[] counts = new int[numClassTypes];
                // Lower partition
                for (int j = 0; j < i; ++j) {
                    counts[classAttribList.get(j).class_.ordinal()] += 1;
                }
                // For each class counts in the lower partition
                int lowPartSize = i;
                for (int count : counts) {
                    if (count <= 0) continue;
                    entropy += (float)lowPartSize / attribs.size() * entropy((float)count / lowPartSize);
                }

                // Clear contents of counts
                Arrays.fill(counts, 0);
                // Upper partition
                for (int j = i; j < attribs.size(); ++j) {
                    counts[classAttribList.get(j).class_.ordinal()] += 1;
                }
                // For each class counts in the upper partition
                int highPartSize = attribs.size() - i;
                for (int count : counts) {
                    if (count <= 0) continue;
                    entropy += (float)highPartSize / attribs.size() * entropy((float)count / highPartSize);
                }

                if (entropy < minEntropy) {
                    minEntropy = entropy;
                    minPartitionIdx = i;
                }
            }

            if (minPartitionIdx > 0) {
                AttribPair<EA> attribPair = new AttribPair<EA>();
                attribPair.left = classAttribList.get(minPartitionIdx - 1).attrib;
                attribPair.right = classAttribList.get(minPartitionIdx).attrib;
                return attribPair;
            }
            return null;
        }
    }

    static class Test {
        enum Attrib0 {
            A,
            B,
            C
        }

        enum Class0 {
            T,
            F
        }

        public static void withDiscreteAttrib() {
            Random random = new Random();
            float thresh = 0.4f;
            ArrayList<Attrib0> attribs = new ArrayList<>(1000);
            ArrayList<Class0> classes = new ArrayList<>(1000);
            for (int i = 0; i < 333; ++i) {
                attribs.add(Attrib0.A);
                if (random.nextDouble() < thresh) {
                    classes.add(Class0.T);
                } else {
                    classes.add(Class0.F);
                }
            }
            for (int i = 333; i < 666; ++i) {
                attribs.add(Attrib0.B);
                if (random.nextDouble() < thresh) {
                    classes.add(Class0.F);
                } else {
                    classes.add(Class0.T);
                }
            }
            for (int i = 666; i < 1000; ++i) {
                attribs.add(Attrib0.C);
                if (random.nextDouble() < thresh) {
                    classes.add(Class0.T);
                } else {
                    classes.add(Class0.F);
                }
            }

            System.out.println(Entropy.forClass(Class0.class, classes));
            System.out.println(Entropy.forAttribDiscrete(Class0.class, Attrib0.class, classes, attribs));
        }

        public static void withContinuousAttrib() {
            Random random = new Random();
            float thresh = 0.1f;
            ArrayList<Integer> attribs = new ArrayList<>(1000);
            ArrayList<Class0> classes = new ArrayList<>(1000);
            int partition = 600;
            for (int i = 0; i < partition; ++i) {
                attribs.add(i);
                if (random.nextDouble() < thresh) {
                    classes.add(Class0.T);
                } else {
                    classes.add(Class0.F);
                }
            }
            for (int i = partition; i < 1000; ++i) {
                attribs.add(i);
                if (random.nextDouble() < thresh) {
                    classes.add(Class0.F);
                } else {
                    classes.add(Class0.T);
                }
            }
            System.out.println(Entropy.forClass(Class0.class, classes));
            Entropy.AttribPair<Integer> pair = Entropy.forAttribContinuous(Class0.class, classes, attribs, new Comparator<Integer>() {
                @Override
                public int compare(Integer arg0, Integer arg1) {
                    return arg0 - arg1;
                }
            });
            System.out.println(pair.left + " " + pair.right);
        }

        public static void main(String[] argv) {
            withContinuousAttrib();
        }
    }
}
