package ESE589.DecisionTree;

import java.util.List;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class filereader {
    public static void read(String fileName) throws IOException {
        List<List<String>> data = new ArrayList<>();
        BufferedReader reader = null;

        try {
            reader = new BufferedReader(new FileReader(fileName));
            String line = reader.readLine();

            while (line != null) {
                List<String> tmt = new ArrayList<>();
                tmt.add(line);
                data.add(tmt);

                line = reader.readLine();

            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();

        }
    }

    public String toString() {

    }
}
