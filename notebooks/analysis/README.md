# Your own analysis notebooks

Name them `NN_topic_initials.ipynb` (e.g. `03_printer_effect_EV.ipynb`) so two people never edit the same file.

Start with:

```python
import sys; sys.path.append('../../src')
from group5_data import load_data, summary
df = load_data()
```
