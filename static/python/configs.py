regions = {"tel aviv": "1",
           "petah tikva": "2",
           "netivot": "3"}

regions_payloads = {"1": {"payload": {"position": [{"lat": "32.0879585",
                                                   "lng": "34.7622266",
                                                    "addressName": "תל אביב",
                                                    "radius": 6}],
                                      "cartId": "CartModels/ce30a1b3-ca0b-4499-8288-16cfbb1070b2"}
                          },
                    "2": {"payload": {"position": [{"lat": 32.084041,
                                                   "lng": 34.887762,
                                                    "addressName": "פתח תקווה, ישראל",
                                                    "radius": 6}],
                                      "cartId": "CartModels/b7d2fa36-688e-4730-be9c-28eecdbeac1d"}},
                    "3": {"payload": {"position": [{"lat": "31.423196",
                                                   "lng": "34.595254",
                                                    "addressName": "נתיבות, ישראל",
                                                    "radius": 6}],
                                      "cartId": "CartModels/02da1938-0643-498c-80ed-c869e570f035"}
                          }
                    }

categories = {"fruits_vegetables": {"category_id": "1",
                                    "translated_name": "פירות וירקות"
                                    },
              "dairy_eggs": {"category_id": "2",
                             "translated_name": "מוצרי חלב וביצים"
                             },
              "meat_fish": {"category_id": "3",
                            "translated_name": "בשר ודגים"
                            },
              "bakery": {"category_id": "4",
                         "translated_name": "מאפים"
                         },
              "salads_sausages": {"category_id": "5",
                                  "translated_name": "סלטים ונקניקים"
                                  },
              "frozen": {"category_id": "6",
                         "translated_name": "קפואים"
                         },
              "cooking": {"category_id": "7",
                          "translated_name": "בישול ואפייה"
                          },
              "spreads_sauces_spices": {"category_id": "8",
                                        "translated_name": "ממרחים, רטבים ותבלינים"
                                        },
              "cereals_snacks": {"category_id": "9",
                                 "translated_name": "חטיפים ודגנים"
                                 },
              "pasta_beans": {"category_id": "10",
                              "translated_name": "שימורים, פסטה וקטניות"
                              },
              "beverages": {"category_id": "11",
                            "translated_name": "משקאות"
                            },
              "babies": {"category_id": "12",
                         "translated_name": "תינוקות"
                         },
              "clean": {"category_id": "13",
                        "translated_name": "ניקיון"
                        },
              "household": {"category_id": "14",
                            "translated_name": "בית ובעלי חיים"
                            },
              "health_beauty": {"category_id": "15",
                                "translated_name": "טיפוח ובריאות"
                                },
}


allowed_mail_suffixes = ["@gmail.com", "@walla.co.il"]

app_secret_key = '12358'

cipher_key = b'widGvVVhNP7IlyanlsoVAcFTNb7XAvPhRxAEaQftSgA='
# to generate a new key use:
# key = Fernet.generate_key()

