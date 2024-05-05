# Decision Tree

## Generated Rule


> First, Accuracy=100% [5/5]
```
feature: age
├── [31...40] -> yes
├── [<=30] ── feature: student
│              ├── [no] -> no
│              └── [yes] -> yes
└── [>40] ── feature: credit_rating
              ├── [excellent] -> no
              └── [fair] -> yes
```

> Second, Accuracy≈91.6% [317/346]  
> 
Rules are skipped due to their length